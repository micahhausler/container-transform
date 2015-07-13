import six

from .schema import TransformationTypes, ARG_MAP

from .compose import ComposeTransformer
from .ecs import ECSTransformer
from .fig import FigTransformer
from .systemd import SystemdTransformer

TRANSFORMER_CLASSES = {
    TransformationTypes.COMPOSE.value: ComposeTransformer,
    TransformationTypes.ECS.value: ECSTransformer,
    TransformationTypes.FIG.value: FigTransformer,
    TransformationTypes.SYSTEMD.value: SystemdTransformer,
}


class Converter(object):

    def __init__(self, filename, input_type, output_type):
        """
        :param filename: The file to be loaded
        :type filename: str
        :param input_type: The output class for the transformer
        :type input_type: str
        :param output_type: The output class for the transformer
        :type output_type: str
        """
        self._filename = filename

        self.input_type = input_type
        self._input_class = TRANSFORMER_CLASSES.get(input_type)
        self.output_type = output_type
        self._output_class = TRANSFORMER_CLASSES.get(output_type)

        self.messages = set()

    def convert(self, verbose=True):
        """
        :rtype: tuple
        :returns: Output containers, messages
        """
        input_transformer = self._input_class(self._filename)
        output_transformer = self._output_class()

        containers = input_transformer.ingest_containers()

        output_containers = []

        for container in containers:
            validated = output_transformer.validate(container)

            converted_container = self._convert_container(
                validated,
                input_transformer,
                output_transformer
            )

            validated = output_transformer.validate(converted_container)

            output_containers.append(validated)

        return output_transformer.emit_containers(output_containers, verbose)

    def _convert_container(self, container, input_transformer, output_transformer):
        """
        Converts a given dictionary to an output container definition

        :type container: dict
        :param container: The container definitions as a dictionary

        :rtype: dict
        :return: A output_type container definition
        """
        output = {}
        for parameter, options in six.iteritems(ARG_MAP):
            output_name = options.get(self.output_type, {}).get('name')
            output_required = options.get(self.output_type, {}).get('required')

            input_name = options.get(self.input_type, {}).get('name')

            if not container.get(input_name) and output_required:
                msg_template = 'Container {name} is missing required parameter "{output_name}".'
                self.messages.add(
                    msg_template.format(
                        output_name=output_name,
                        output_type=self.output_type,
                        name=container.get('name', container)
                    )
                )

            if container.get(input_name) and \
                    hasattr(input_transformer, 'ingest_{}'.format(parameter)) and \
                    output_name and hasattr(output_transformer, 'emit_{}'.format(parameter)):
                # call transform_{}
                ingest_func = getattr(input_transformer, 'ingest_{}'.format(parameter))
                emit_func = getattr(output_transformer, 'emit_{}'.format(parameter))

                output[output_name] = emit_func(ingest_func(container.get(input_name)))

        return output
