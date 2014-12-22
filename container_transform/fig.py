from copy import deepcopy
import six
import yaml

from .schema import TransformationTypes
from .transformer import BaseTransformer


class FigTransformer(BaseTransformer):
    """
    A transformer for Fig

    To use this class:

    .. code-block:: python

        transformer = FigTransformer('./fig.yml')
        output = transformer.transform()
        print(json.dumps(output, indent=4))

    """
    input_type = TransformationTypes.FIG.value

    def read_stream(self, stream):
        return yaml.safe_load(stream=stream)

    def transform(self, input_data=None):
        """
        Transform the YAML into an ECS task
        """
        input_data = input_data or self.stream or {}

        output_containers = []

        for container_name, definition in six.iteritems(input_data):
            definition = definition.copy()

            definition['name'] = container_name
            container = self.convert_container(definition)
            container['name'] = container_name
            container['essential'] = True

            output_containers.append(container)

        return output_containers

    def _parse_port_mapping(self, mapping):
        parts = str(mapping).split(':')
        if len(parts) == 1:
            return {
                "hostPort": int(parts[0]),
                "containerPort": int(parts[0])
            }
        elif len(parts) == 2:
            return {
                "hostPort": int(parts[0]),
                "containerPort": int(parts[1])
            }
        else:
            original_parts = deepcopy(parts)
            for part in parts:
                if '.' in part:
                    original_parts.remove(part)
            return self._parse_port_mapping(':'.join(original_parts))

    def transform_port_mappings(self, port_mappings):
        """
        Transform the fig port mappings to ECS mappings

        :param port_mappings: The fig port mappings
        :type port_mappings: list
        :return: the ECS port mappings
        :rtype: list
        """
        return [self._parse_port_mapping(mapping) for mapping in port_mappings]

    def transform_memory(self, memory):
        """
        Transform the memory into MB

        :param memory: Fig memory definition. (1g, 24k)
        :type memory: str
        :return: The memory in MB
        :rtype: int
        """

        def lshift(num, shift):
            return num << shift

        def rshift(num, shift):
            return num >> shift

        bit_shift = {
            'g': {'func': lshift, 'shift': 10},
            'm': {'func': lshift, 'shift': 0},
            'k': {'func': rshift, 'shift': 10},
            'b': {'func': rshift, 'shift': 20}
        }
        unit = memory[-1]
        number = int(memory[:-1])
        mem_in_mb = bit_shift[unit]['func'](number, bit_shift[unit]['shift'])
        if mem_in_mb < 4:
            return 4
        else:
            return mem_in_mb

    def transform_cpu(self, cpu):
        pass  # pragma: no cover

    def transform_environment(self, environment):
        """
        Transform the fig environment into an ECS environment list

        :param environment: The Fig environment
        :type environment: dict or list
        :rtype: list of dict
        """
        data = []
        if type(environment) is list:
            for kv in environment:
                index = kv.find('=')
                data.append({
                    'name': str(kv[:index]),
                    'value': str(kv[index + 1:])
                })
        if type(environment) is dict:
            for key, value in six.iteritems(environment):
                data.append({'name': str(key), 'value': str(value)})
        return data

    def transform_command(self, command):
        return command.split()

    def transform_entrypoint(self, entrypoint):
        return entrypoint.split()
