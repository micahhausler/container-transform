import six

from abc import ABCMeta, abstractmethod

"""The SCHEMA defines the argument format the .ingest_*() and .emit_*()
methods should produce and accept (respectively)"""
SCHEMA = {
    'image': str,
    'name': str,
    'cpu': int,  # out of 1024
    'memory': int,  # in bytes
    'links': list,  # This is universal across formats
    'port_mappings': {
        'host_ip': str,
        'host_port': int,
        'container_ip': str,
        'container_port': int
    },
    'environment': dict,  # A simple key: value dictionary
    'entrypoint': str,  # An unsplit string
    'command': str,  # An unsplit string
    'volumes_from': list,  # A list of containers, ignoring read_only
    'volumes': list,  # A list of dict {'host': '/path', 'container': '/path', 'readonly': True}
}


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

    @abstractmethod
    def emit_containers(self, containers, verbose=True):
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

    def ingest_name(self, name):
        return name

    def emit_name(self, name):
        return name

    def ingest_image(self, image):
        return image

    def emit_image(self, image):
        return image

    def ingest_links(self, image):
        return image

    def emit_links(self, image):
        return image

    @abstractmethod
    def ingest_port_mappings(self, port_mappings):
        raise NotImplementedError

    @abstractmethod
    def emit_port_mappings(self, port_mappings):
        raise NotImplementedError

    @abstractmethod
    def ingest_cpu(self, cpu):
        raise NotImplementedError

    @abstractmethod
    def emit_cpu(self, cpu):
        raise NotImplementedError

    @abstractmethod
    def ingest_memory(self, memory):
        raise NotImplementedError

    @abstractmethod
    def emit_memory(self, memory):
        raise NotImplementedError

    @abstractmethod
    def ingest_environment(self, environment):
        raise NotImplementedError

    @abstractmethod
    def emit_environment(self, environment):
        raise NotImplementedError

    @abstractmethod
    def ingest_command(self, command):
        raise NotImplementedError

    @abstractmethod
    def emit_command(self, command):
        raise NotImplementedError

    @abstractmethod
    def ingest_entrypoint(self, entrypoint):
        raise NotImplementedError

    @abstractmethod
    def emit_entrypoint(self, entrypoint):
        raise NotImplementedError

    @abstractmethod
    def ingest_volumes_from(self, volumes_from):
        raise NotImplementedError

    @abstractmethod
    def emit_volumes_from(self, volumes_from):
        raise NotImplementedError

    @abstractmethod
    def ingest_volumes(self, volumes):
        raise NotImplementedError

    @abstractmethod
    def emit_volumes(self, volumes):
        raise NotImplementedError
