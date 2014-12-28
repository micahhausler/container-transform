import six

from abc import ABCMeta, abstractmethod


class BaseTransformer(six.with_metaclass(ABCMeta), object):
    """
    The base class for Transformer classes to inherit from.

    Basic usage should look like

    .. code-block:: python

        transformer = MyTransformer('./my-file.txt')
        normalized_keys = transformer.ingest_containers()

    """
    def __init__(self, filename=None):
        """
        :param filename: The file to be loaded
        :type filename: str
        """
        stream = None
        if filename:
            self._filename = filename
            stream = self._read_file(filename)
        self.stream = stream

    def _read_file(self, filename):
        """
        :param filename: The location of the file to read
        :type filename: str
        """
        with open(filename, 'r') as stream:
            return self._read_stream(stream=stream)

    @abstractmethod
    def _read_stream(self, stream):
        """
        Override this method and parse the stream to be passed to
        ``self.transform()``

        :param stream: A file-like object
        :type stream: file
        """
        raise NotImplementedError

    @abstractmethod
    def ingest_containers(self, containers=None):
        """
        Ingest self.stream and return a list of un-converted container
        definitions dictionaries.

        This is to normalize `where` all the container information is.
        For example, Fig places the container name outside the rest of the
        container definition. We need to have a 'name' key in the container
        definition.

        :rtype: list of dict
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def emit_containers(containers, verbose=True):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def validate(container):
        """
        Validate that the container has all essential parameters and add any if
        possible

        :param container: The converted container
        :type container: dict

        :return: The container with all valid parameters
        :rtype: dict
        """
        raise NotImplementedError

    @staticmethod
    def ingest_name(name):
        return name

    @staticmethod
    def emit_name(name):
        return name

    @staticmethod
    def ingest_image(image):
        return image

    @staticmethod
    def emit_image(image):
        return image

    @staticmethod
    def ingest_links(image):
        return image

    @staticmethod
    def emit_links(image):
        return image

    @staticmethod
    @abstractmethod
    def ingest_port_mappings(port_mappings):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def emit_port_mappings(port_mappings):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def ingest_cpu(cpu):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def emit_cpu(cpu):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def ingest_memory(memory):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def emit_memory(memory):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def ingest_environment(environment):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def emit_environment(environment):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def ingest_command(command):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def emit_command(command):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def ingest_entrypoint(entrypoint):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def emit_entrypoint(entrypoint):
        raise NotImplementedError
