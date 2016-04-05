import uuid
from functools import reduce

import yaml

from .transformer import BaseTransformer


class ComposeTransformer(BaseTransformer):
    """
    A transformer for docker-compose v1 and v2

    To use this class:

    .. code-block:: python

        transformer = ComposeTransformer('./docker-compose.yml')
        normalized_keys = transformer.ingest_containers()

    """
    def __init__(self, filename=None):
        """
        We override ``.__init__()`` on purpose, we need to get the volume,
        version, network, and possibly other data.

        :param filename: The file to be loaded
        :type filename: str
        """
        if filename:
            self._filename = filename
            stream = self._read_file(filename)
            self.stream_version = int(stream.get('version', '1'))

            if self.stream_version > 1:
                self.stream = stream.get('services')
                self.volumes = stream.get('volumes', None)
                self.networks = stream.get('networks', None)
            else:
                self.stream = stream
        else:
            self.stream = None

    def _read_stream(self, stream):
        return yaml.safe_load(stream=stream)

    def ingest_containers(self, containers=None):
        """
        Transform the YAML into a dict with normalized keys
        """
        containers = containers or self.stream or {}

        output_containers = []

        for container_name, definition in containers.items():
            container = definition.copy()
            container['name'] = container_name
            output_containers.append(container)

        return output_containers

    def emit_containers(self, containers, verbose=True):

        services = {}
        for container in containers:
            name_in_container = container.get('name')
            if not name_in_container:
                name = str(uuid.uuid4())
            else:
                name = container.pop('name')
            services[name] = container

        output = {
            'services': services,
            'version': '2',
        }

        noalias_dumper = yaml.dumper.SafeDumper
        noalias_dumper.ignore_aliases = lambda self, data: True
        return yaml.dump(
            output,
            default_flow_style=False,
            Dumper=noalias_dumper
        )

    @staticmethod
    def validate(container):

        return container

    @staticmethod
    def _parse_port_mapping(mapping):
        parts = str(mapping).split(':')
        if len(parts) == 1:
            return {
                'container_port': int(parts[0])
            }
        if len(parts) == 2 and '.' not in mapping:
            return {
                'host_port': int(parts[0]),
                'container_port': int(parts[1])
            }
        if len(parts) == 3:
            if '.' in parts[0]:
                return {
                    'host_ip': parts[0],
                    'host_port': int(parts[1]),
                    'container_port': int(parts[2])
                }
            else:
                return {
                    'host_port': int(parts[0]),
                    'container_ip': parts[1],
                    'container_port': int(parts[2])
                }
        if len(parts) == 4:
            return {
                'host_ip': parts[0],
                'host_port': int(parts[1]),
                'container_ip': parts[2],
                'container_port': int(parts[3])
            }

    def ingest_port_mappings(self, port_mappings):
        """
        Transform the docker-compose port mappings to base schema port_mappings

        :param port_mappings: The compose port mappings
        :type port_mappings: list
        :return: the base schema port_mappings
        :rtype: list of dict
        """
        return [self._parse_port_mapping(mapping) for mapping in port_mappings]

    @staticmethod
    def _emit_mapping(mapping):
        parts = []
        if mapping.get('host_ip'):
            parts.append(str(mapping['host_ip']))
        if mapping.get('host_port'):
            parts.append(str(mapping['host_port']))
        if mapping.get('container_ip'):
            parts.append(str(mapping['container_ip']))
        if mapping.get('container_port'):
            parts.append(str(mapping['container_port']))
        return ':'.join(parts)

    def emit_port_mappings(self, port_mappings):
        """
        :param port_mappings: the base schema port_mappings
        :type port_mappings: list of dict
        :return:
        :rtype: list of str
        """
        return [str(self._emit_mapping(mapping)) for mapping in port_mappings]

    def ingest_memory(self, memory):
        """
        Transform the memory into bytes

        :param memory: Compose memory definition. (1g, 24k)
        :type memory: memory string or integer
        :return: The memory in bytes
        :rtype: int
        """
        def lshift(num, shift):
            return num << shift

        def rshift(num, shift):
            return num >> shift

        if isinstance(memory, int):
            # Memory was specified as an integer, meaning it is in bytes
            memory = '{}b'.format(memory)

        bit_shift = {
            'g': {'func': lshift, 'shift': 30},
            'm': {'func': lshift, 'shift': 20},
            'k': {'func': lshift, 'shift': 10},
            'b': {'func': rshift, 'shift': 0}
        }
        unit = memory[-1]
        number = int(memory[:-1])
        return bit_shift[unit]['func'](number, bit_shift[unit]['shift'])

    def emit_memory(self, memory):
        return '{}b'.format(memory)

    def ingest_cpu(self, cpu):
        return cpu

    def emit_cpu(self, cpu):
        return cpu

    def ingest_environment(self, environment):
        output = {}
        if type(environment) is list:
            for kv in environment:
                index = kv.find('=')
                output[str(kv[:index])] = str(kv[index + 1:])
        if type(environment) is dict:
            for key, value in environment.items():
                output[str(key)] = str(value)
        return output

    def emit_environment(self, environment):
        return environment

    def ingest_command(self, command):
        return command

    def emit_command(self, command):
        return command

    def ingest_entrypoint(self, entrypoint):
        return entrypoint

    def emit_entrypoint(self, entrypoint):
        return entrypoint

    def ingest_volumes_from(self, volumes_from):
        ingested_volumes_from = []
        for vol in volumes_from:
            ingested = {}
            parts = vol.split(':')
            rwo_value = None

            assert(len(parts) <= 3)

            if len(parts) == 3:
                # Is form 'service:name:ro' or 'container:name:ro'
                # in new compose v2 format.
                source_container, rwo_value = parts[1:]
            elif len(parts) == 2:
                # Is form 'name:ro' or 'service:name' (for >= v2)
                if self.stream_version > 1 and parts[0] == 'service':
                    source_container = parts[1]
                else:
                    assert(parts[1] in ['ro', 'rw'])
                    source_container = parts[0]
                    rwo_value = parts[1]
            else:
                source_container = parts[0]

            if rwo_value == 'ro':
                ingested['read_only'] = True

            ingested['source_container'] = source_container
            ingested_volumes_from.append(ingested)

        return ingested_volumes_from

    def emit_volumes_from(self, volumes_from):
        return volumes_from

    @staticmethod
    def _ingest_volume(volume):
        parts = volume.split(':')

        if len(parts) == 1:
            return {
                'host': parts[0],
                'container': parts[0]
            }
        if len(parts) == 2 and parts[1] != 'ro':
            return {
                'host': parts[0],
                'container': parts[1]
            }
        if len(parts) == 2 and parts[1] == 'ro':
            return {
                'host': parts[0],
                'container': parts[0],
                'readonly': True
            }
        if len(parts) == 3 and parts[-1] == 'ro':
            return {
                'host': parts[0],
                'container': parts[1],
                'readonly': True
            }

    def ingest_volumes(self, volumes):
        return [
            self._ingest_volume(volume)
            for volume
            in volumes
            if self._ingest_volume(volume) is not None
        ]

    @staticmethod
    def _emit_volume(volume):
        volume_str = volume.get('host') + ':' + volume.get('container', ':')
        volume_str = volume_str.strip(':')

        if volume.get('readonly') and len(volume_str):
            volume_str += ':ro'
        return volume_str

    def emit_volumes(self, volumes):
        return [
            self._emit_volume(volume)
            for volume
            in volumes
            if len(self._emit_volume(volume))
        ]

    @staticmethod
    def _parse_label_string(label):
        eq = label.find('=')
        if eq == -1:
            return {label: None}
        else:
            return {label[:eq]: label[eq+1:]}

    def ingest_labels(self, labels):
        if isinstance(labels, list):
            return reduce(
                lambda a, b: a.update(b) or a,
                map(self._parse_label_string, labels),
                {}
            )
        return labels

    def emit_labels(self, labels):
        return labels

    def ingest_logging(self, logging):
        return logging

    def emit_logging(self, logging):
        return logging
