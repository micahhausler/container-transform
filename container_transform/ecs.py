import json
import uuid

import six

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
    input_type = TransformationTypes.FIG.value

    def _read_stream(self, stream):
        return json.load(stream)

    def ingest_containers(self, containers=None):
        containers = containers or self.stream or {}
        return containers

    @staticmethod
    def emit_containers(containers, verbose=True):
        if verbose:
            return json.dumps(containers, indent=4)
        else:
            return json.dumps(containers)

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
        return {
            'host_port': int(mapping['hostPort']),
            'container_port': int(mapping['containerPort'])
        }

    @staticmethod
    def ingest_port_mappings(port_mappings):
        """
        Transform the ECS mappings to base schema mappings

        :param port_mappings: The ECS port mappings
        :type port_mappings: list of dict
        :return: The base schema mappings
        :rtype: list of dict
        """
        return [ECSTransformer._parse_port_mapping(mapping) for mapping in port_mappings]

    @staticmethod
    def _emit_mapping(mapping):
        if len(mapping) == 1:
            return {
                'hostPort': int(list(mapping.values())[0]),
                'containerPort': int(list(mapping.values())[0]),
            }

        return {
            'hostPort': int(mapping['host_port']),
            'containerPort': int(mapping['container_port']),
        }

    @staticmethod
    def emit_port_mappings(port_mappings):
        return [ECSTransformer._emit_mapping(mapping) for mapping in port_mappings]

    @staticmethod
    def ingest_memory(memory):
        return memory << 20

    @staticmethod
    def emit_memory(memory):
        mem_in_mb = memory >> 20

        if 4 > mem_in_mb:
            return 4
        return mem_in_mb

    @staticmethod
    def ingest_cpu(cpu):
        return cpu

    @staticmethod
    def emit_cpu(cpu):
        return cpu

    @staticmethod
    def ingest_environment(environment):
        output = {}
        for kv in environment:
            output[kv['name']] = kv['value']
        return output

    @staticmethod
    def emit_environment(environment):
        output = []
        for k, v in six.iteritems(environment):
            output.append({'name': k, 'value': v})
        return output

    @staticmethod
    def ingest_command(command):
        return ' '.join(command)

    @staticmethod
    def emit_command(command):
        return command.split()

    @staticmethod
    def ingest_entrypoint(entrypoint):
        return ' '.join(entrypoint)

    @staticmethod
    def emit_entrypoint(entrypoint):
        return entrypoint.split()

    @staticmethod
    def ingest_volumes_from(volumes_from):
        return [vol['sourceContainer'] for vol in volumes_from]

    @staticmethod
    def emit_volumes_from(volumes_from):
        return [{'sourceContainer': vol} for vol in volumes_from]
