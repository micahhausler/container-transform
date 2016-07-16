import json
import uuid
from copy import copy

from .schema import TransformationTypes
from .transformer import BaseTransformer


class ECSTransformer(BaseTransformer):
    """
    A transformer for ECS Tasks

    To use this class:

    .. code-block:: python

        transformer = ECSTransformer('./task.json')
        output = transformer.ingest_containers()
        print(json.dumps(output, indent=4))

    """
    input_type = TransformationTypes.COMPOSE.value

    def __init__(self, filename=None):
        """
        We override ``.__init__()`` on purpose, we need to get the volume data.

        :param filename: The file to be loaded
        :type filename: str
        """
        family, stream, volumes_in = '', None, []
        if filename:
            self._filename = filename
            family, stream, volumes_in = self._read_file(filename)
        self.family = family
        self.stream = stream
        self.volumes_in = volumes_in

        self.volumes = []

    def _read_stream(self, stream):
        """
        We override the return signature of
        ``super(BaseTransformer, self)._read_stream()`` to return extra volume
        data. This is intentional.

        :param stream: A file like object
        :returns: Return the family name, containers, and volumes. If there are
            no volumes or family name, a tuple of ('', dict, []) is
            returned
        :rtype: tuple of (str, list of dict, list of dict)

        """
        contents = json.load(stream)

        family, containers, volumes = '', contents, []

        if isinstance(contents, dict) and 'containerDefinitions' in contents.keys():
            family = contents.get('family', None)
            containers = contents.get('containerDefinitions', [])
            volumes = self.ingest_volumes_param(contents.get('volumes', []))

        return family, containers, volumes

    def ingest_containers(self, containers=None):
        containers = containers or self.stream or {}
        return containers

    def add_volume(self, volume):
        """
        Add a volume to self.volumes if it isn't already present
        """
        for old_vol in self.volumes:
            if volume == old_vol:
                return
        self.volumes.append(volume)

    def emit_containers(self, containers, verbose=True):
        """
        Emits the task definition and sorts containers by name

        :param containers: List of the container definitions
        :type containers: list of dict

        :param verbose: Print out newlines and indented JSON
        :type verbose: bool

        :returns: The text output
        :rtype: str
        """
        containers = sorted(containers, key=lambda c: c.get('name'))
        task_definition = {
            'family': self.family,
            'containerDefinitions': containers,
            'volumes': self.volumes or []
        }
        if verbose:
            return json.dumps(task_definition, indent=4, sort_keys=True)
        else:
            return json.dumps(task_definition)

    @staticmethod
    def validate(container):
        container['essential'] = True

        container_name = container.get('name')

        if not container_name:
            container_name = str(uuid.uuid4())
            container['name'] = container_name
        return container

    @staticmethod
    def _parse_port_mapping(mapping):
        output = {
            'container_port': int(mapping['containerPort']),
            'protocol': mapping.get('protocol', 'tcp')
        }
        host_port = mapping.get('hostPort')
        if host_port:
            output['host_port'] = host_port

        return output

    def ingest_port_mappings(self, port_mappings):
        """
        Transform the ECS mappings to base schema mappings

        :param port_mappings: The ECS port mappings
        :type port_mappings: list of dict
        :return: The base schema mappings
        :rtype: list of dict
        """
        return [self._parse_port_mapping(mapping) for mapping in port_mappings]

    @staticmethod
    def _emit_mapping(mapping):
        output = {}
        if 'host_port' not in mapping:
            output.update({
                'containerPort': int(mapping.get('container_port')),
            })
        else:
            output.update({
                'hostPort': int(mapping['host_port']),
                'containerPort': int(mapping['container_port']),
            })
        if mapping.get('protocol') == 'udp':
            output['protocol'] = 'udp'
        return output

    def emit_port_mappings(self, port_mappings):
        return [self._emit_mapping(mapping) for mapping in port_mappings]

    def ingest_memory(self, memory):
        return memory << 20

    def emit_memory(self, memory):
        mem_in_mb = memory >> 20

        if 4 > mem_in_mb:
            return 4
        return mem_in_mb

    def ingest_cpu(self, cpu):
        return cpu

    def emit_cpu(self, cpu):
        return cpu

    def ingest_environment(self, environment):
        output = {}
        for kv in environment:
            output[kv['name']] = kv['value']
        return output

    def emit_environment(self, environment):
        output = []
        for k, v in environment.items():
            output.append({'name': k, 'value': v})
        return output

    def ingest_command(self, command):
        return ' '.join(command)

    def emit_command(self, command):
        return command.split()

    def ingest_entrypoint(self, entrypoint):
        return ' '.join(entrypoint)

    def emit_entrypoint(self, entrypoint):
        return entrypoint.split()

    def ingest_volumes_from(self, volumes_from):
        return [vol['sourceContainer'] for vol in volumes_from]

    def emit_volumes_from(self, volumes_from):
        emitted = []
        volumes_from = copy(volumes_from)
        for vol in volumes_from:
            emit = {}
            if vol.get('read_only'):
                emit['readOnly'] = vol['read_only']
            emit['sourceContainer'] = vol['source_container']
            emitted.append(emit)
        return emitted

    def ingest_volumes_param(self, volumes):
        """
        This is for ingesting the "volumes" of a task description
        """
        data = {}

        for volume in volumes:
            if volume.get('host', {}).get('sourcePath'):
                data[volume.get('name')] = {
                    'path': volume.get('host', {}).get('sourcePath'),
                    'readonly': volume.get('readOnly', False)
                }
            else:
                data[volume.get('name')] = {
                    'path': '/tmp/{}'.format(uuid.uuid4().hex[:8]),
                    'readonly': volume.get('readOnly', False)
                }
        return data

    def _ingest_volume(self, volume):
        data = {
            'host': self.volumes_in.get(volume.get('sourceVolume')).get('path'),
            'container': volume.get('containerPath'),
            'readonly': self.volumes_in.get(volume.get('sourceVolume')).get('readonly')
        }
        return data

    def ingest_volumes(self, volumes):
        return [self._ingest_volume(volume) for volume in volumes]

    @staticmethod
    def path_to_name(path):
        return path.replace('/', ' ').title().replace(' ', '').replace('.', '_')

    def _build_volume(self, volume):
        host_path = volume.get('host')
        return {
            'name': self.path_to_name(host_path),
            'host': {
                'sourcePath': host_path
            }
        }

    def _build_mountpoint(self, volume):
        """
        Given a generic volume definition, create the mountPoints element
        """
        self.add_volume(self._build_volume(volume))
        return {
            'sourceVolume': self.path_to_name(volume.get('host')),
            'containerPath': volume.get('container')
        }

    def emit_volumes(self, volumes):
        return [
            self._build_mountpoint(volume)
            for volume
            in volumes
            if self._build_mountpoint(volume) is not None
        ]

    def ingest_labels(self, labels):
        return labels

    def emit_labels(self, labels):
        return labels

    def ingest_logging(self, logging):
        data = logging
        if data.get('logDriver'):  # pragma: no cover
            data['driver'] = data.get('logDriver')
            del data['logDriver']
        return logging

    def emit_logging(self, logging):
        data = logging
        if data.get('driver'):  # pragma: no cover
            data['logDriver'] = data.get('driver')
            del data['driver']
        return logging
