import uuid

import yaml

from .transformer import BaseTransformer


class ComposeTransformer(BaseTransformer):
    """
    A transformer for docker-compose

    To use this class:

    .. code-block:: python

        transformer = ComposeTransformer('./docker-compose.yml')
        normalized_keys = transformer.ingest_containers()

    """

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

        output = {}
        for container in containers:
            name_in_container = container.get('name')
            if not name_in_container:
                name = str(uuid.uuid4())
            else:
                name = container.pop('name')
            output[name] = container

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
        :type memory: str
        :return: The memory in bytes
        :rtype: int
        """
        def lshift(num, shift):
            return num << shift

        def rshift(num, shift):
            return num >> shift

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
        return volumes_from

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
