from abc import ABCMeta, abstractproperty, abstractmethod

import six

from .schema import TransformationTypes, ARG_MAP


class BaseTransformer(six.with_metaclass(ABCMeta), object):
    """
    The base class for Transformer classes to inherit from.

    Basic usage should look like

    .. code-block:: python

        transformer = MyTransformer('./my-file.txt')
        output = transformer.transform()
        print(json.dumps(output, indent=4))

    """
    def __init__(self, filename, output_type=None):
        """
        :param filename: The file to be loaded
        :type filename: str
        :param output_type: The output type for the transformer
        :type output_type: str
        """
        self._filename = filename
        self.stream = self.read_file(filename)

        self.messages = set()
        self.output_type = output_type or TransformationTypes.ECS.value

    @abstractproperty
    def input_type(self):
        raise NotImplementedError

    def read_file(self, filename):
        """
        :param filename: The location of the file to read
        :type filename: str
        """
        with open(filename, 'r') as stream:
            return self.read_stream(stream=stream)

    def convert_container(self, container):
        """
        Converts a given dictionary to an output container definition

        :type container: dict
        :param container: The container definitions as a dictionary

        :rtype: dict
        :return: A output_type container definition
        """
        output = {}
        for parameter, options in six.iteritems(ARG_MAP):
            if options.get(self.output_type) and options.get(self.input_type):
                container_value = container.get(options[self.input_type])
                if container_value:
                    # This branch covers when the input type and the output type
                    # have a parameter valid to both
                    if hasattr(self, 'transform_{}'.format(parameter)):
                        func = getattr(self, 'transform_{}'.format(parameter))
                        output[options[self.output_type]] = func(container_value)
                    else:
                        output[options[self.output_type]] = container_value
            elif not options.get(self.output_type) and options.get(self.input_type):
                container_value = container.get(options[self.input_type])
                if container_value:
                    # This branch covers when the input type has an parameter that the
                    # output type does not have defined
                    container_name = container.get('name', None)

                    parameter_ignored_template = (
                        'The output type {output_type} does not support the '
                        'parameter \'{parameter}\'. The parameter \'{k}\': \'{v}\''
                        ' will be ignored'
                    )

                    message = parameter_ignored_template.format(
                        output_type=self.output_type,
                        parameter=parameter,
                        k=options[self.input_type],
                        v=container_value
                    )
                    if container_name:
                        message += ' for container {}.'.format(container_name)
                    else:
                        message += '.'

                    self.messages.add(message)
        return output

    @abstractmethod
    def read_stream(self, stream):
        """
        Override this method and parse the stream to be passed to ``self.transform()``

        :param stream: A file-like object
        :type stream: file
        """
        raise NotImplementedError

    @abstractmethod
    def transform(self, input_data=None):
        """
        Override this method and iteratively call ``self.convert_container()`` to transform
        all input from the input stream to an ECS config.
        """
        raise NotImplementedError

    @abstractmethod
    def transform_port_mappings(self, port_mappings):
        """
        Override this to transform port mappings
        """
        raise NotImplementedError

    @abstractmethod
    def transform_cpu(self, cpu):
        """
        Override this to transform CPU
        """
        raise NotImplementedError

    @abstractmethod
    def transform_memory(self, memory):
        """
        Override this to transform memory
        """
        raise NotImplementedError

    @abstractmethod
    def transform_environment(self, environment):
        """
        Override this to transform environment variables
        """
        raise NotImplementedError

    @abstractmethod
    def transform_command(self, command):
        """
        Override this to transform the runtime CMD
        """
        raise NotImplementedError

    @abstractmethod
    def transform_entrypoint(self, entrypoint):
        """
        Override this to transform the container entrypoint
        """
        raise NotImplementedError
