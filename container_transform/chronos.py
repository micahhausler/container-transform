import json
import uuid

from datetime import datetime

from copy import deepcopy
from functools import reduce
from collections import Mapping, defaultdict

from .schema import TransformationTypes, ARG_MAP
from .transformer import BaseTransformer


def update_nested_dict(d, u):
    for k, v in u.items():
        if isinstance(v, Mapping):
            r = update_nested_dict(d.get(k, {}), v)
            d[k] = r
        elif isinstance(v, list):
            if not d.get(k):
                d[k] = v
            else:
                d[k] += v
        else:
            d[k] = u[k]
    return d


def lookup_nested_dict(dic, key, *keys):
    if keys:
        return lookup_nested_dict(dic.get(key, None), *keys)
    return dic.get(key)


class ChronosTransformer(BaseTransformer):
    """
    A transformer for Chronos Jobs

    When consuming Chronos input, the transformer supports:

    When emitting Chronos output, the transformer will emit a list of
    applications if there is more than one. Otherwise, it will emit a single
    application.

    To use this class:

    .. code-block:: python

        transformer = ChronosTransformer('./task.json')
        output = transformer.ingest_container()
        print(json.dumps(output, indent=4))

    """
    input_type = TransformationTypes.COMPOSE.value

    def __init__(self, filename=None):
        """
        :param filename: The file to be loaded
        :type filename: str
        """
        if filename:
            self._filename = filename
            stream = self._read_file(filename)
            self.stream = stream
        else:
            self.stream = None

    def _read_stream(self, stream):
        """
        Read in the json stream
        """
        return json.load(stream)

    def _lookup_parameter(self, container, key, common_type=None):
        """
        Lookup the `docker run` keyword from the 'container.docker.parameters' list
        :param container: The container in question
        :param key: The key name we're looking up
        :param is_list: if the response is a list of items
        """
        if not container.get('container', {}).get('parameters'):
            return
        params = container['container']['parameters']

        # Super hacky - log-opt is a sub option of the logging directive of everything else
        if key == 'log-driver':
            return [
                p
                for p
                in params
                if p['key'] in ['log-opt', 'log-driver']]

        matching_params = [
            p['value']
            for p
            in params
            if p['key'] == key]

        if matching_params:
            if common_type == list:
                return matching_params
            else:
                return matching_params[0]

    def flatten_container(self, container):
        """
        Accepts a chronos container and pulls out the nested values into the top level
        """
        for names in ARG_MAP.values():
            if names[TransformationTypes.CHRONOS.value]['name'] and \
                            '.' in names[TransformationTypes.CHRONOS.value]['name']:
                chronos_dotted_name = names[TransformationTypes.CHRONOS.value]['name']
                parts = chronos_dotted_name.split('.')

                if parts[-2] == 'parameters':
                    # Special lookup for docker parameters
                    common_type = names[TransformationTypes.CHRONOS.value].get('type')
                    result = self._lookup_parameter(container, parts[-1], common_type)
                    if result:
                        container[chronos_dotted_name] = result
                else:
                    result = lookup_nested_dict(container, *parts)
                    if result:
                        container[chronos_dotted_name] = result
        return container

    def ingest_containers(self, containers=None):
        containers = containers or self.stream or {}
        # Accept lists of tasks for convenience
        if isinstance(containers, dict):
            containers = [containers]
        return [
            self.flatten_container(container)
            for container
            in containers]

    def emit_containers(self, containers, verbose=True):
        """
        Emits the applications and sorts containers by name

        :param containers: List of the container definitions
        :type containers: list of dict

        :param verbose: Print out newlines and indented JSON
        :type verbose: bool

        :returns: The text output
        :rtype: str
        """
        containers = sorted(containers, key=lambda c: c.get('name'))

        if len(containers) == 1 and isinstance(containers, list):
            containers = containers[0]

        if verbose:
            return json.dumps(containers, indent=4, sort_keys=True)
        else:
            return json.dumps(containers)

    def validate(self, container):
        # Ensure container name
        container_name = container.get('name', str(uuid.uuid4()))
        container['name'] = container_name

        container_data = defaultdict(lambda: defaultdict(dict))
        container_data.update(container)

        # Find keys with periods in the name, these are keys that we delete and
        # create the corresponding entry for
        for key, value in deepcopy(container_data).items():
            if key.startswith('container.'):
                parts = key.split('.')

                if parts[-2] == 'parameters':
                    # Parameters are inserted below
                    parts = parts[:-1]
                    data = reduce(lambda x, y: {y: x}, reversed(parts + [value]))
                    update_nested_dict(container_data, data)
                    del container_data[key]
                else:
                    data = reduce(lambda x, y: {y: x}, reversed(parts + [value]))
                    update_nested_dict(container_data, data)
                    del container_data[key]

        # Sort the parameters in a deterministic way
        if container_data['container'].get('parameters'):
            old_params = container_data['container']['parameters']
            sorted_values = sorted(
                old_params, key=lambda p: str(p.get('value'))
            )
            sorted_keys = sorted(
                sorted_values, key=lambda p: p.get('key')
            )
            container_data['container']['parameters'] = sorted_keys

        # Assume the network mode is BRIDGE if unspecified
        if container_data['container'].get('network') != 'HOST':
            container_data['container']['network'] = 'BRIDGE'

        container_data['container']['forcePullImage'] = True
        container_data['container']['type'] = 'DOCKER'
        container_data['uris'] = []
        container_data['schedule'] = 'R/{now}/PT1H'.format(now=datetime.utcnow().isoformat())
        container_data['disabled'] = False
        container_data['shell'] = False
        container_data['owner'] = None
        container_data['ownerName'] = None
        container_data['description'] = ""

        return container_data

    def ingest_name(self, name):
        return name.split('/')[-1]

    def emit_links(self, links):
        return [
            {'key': 'link', 'value': link}
            for link
            in links
        ]

    @staticmethod
    def _parse_port_mapping(mapping):
        protocol = 'udp' if 'udp' in str(mapping) else 'tcp'
        output = {
            'protocol': protocol
        }
        mapping = str(mapping).rstrip('/udp')
        parts = str(mapping).split(':')
        if len(parts) == 1:
            output.update({
                'container_port': int(parts[0])
            })
        else:
            output.update({
                'host_port': int(parts[0]),
                'container_port': int(parts[1]),
            })
        return output

    def ingest_port_mappings(self, port_mappings):
        """
        Transform the port mappings to base schema mappings

        :param port_mappings: The port mappings
        :type port_mappings: list of dict
        :return: The base schema mappings
        :rtype: list of dict
        """
        return [self._parse_port_mapping(mapping) for mapping in port_mappings]

    def _construct_port_mapping(self, mapping):
        output = str(mapping['container_port'])
        if 'host_port' in mapping:
            output = str(mapping['host_port']) + ':' + output
        if mapping.get('protocol') == 'udp':
            output += '/udp'
        return output

    def emit_port_mappings(self, port_mappings):
        return [
            {
                'key': 'publish',
                'value': self._construct_port_mapping(mapping),
            }
            for mapping
            in port_mappings]

    def ingest_memory(self, memory):
        return memory << 20

    def emit_memory(self, memory):
        mem_in_mb = memory >> 20
        if 4 > mem_in_mb:
            return 4
        return mem_in_mb

    def ingest_cpu(self, cpu):
        return float(cpu * 1024)

    def emit_cpu(self, cpu):
        return float(cpu/1024)

    def ingest_environment(self, environment):
        return dict([(var['name'], var['value']) for var in environment])

    def emit_environment(self, environment):
        environ = [
            {'name': name, 'value': value}
            for name, value
            in environment.items()
        ]
        # Sort the parameters in a deterministic way
        sorted_by_value = sorted(environ, key=lambda p: p.get('value'))
        return sorted(sorted_by_value, key=lambda p: p.get('name'))

    def ingest_command(self, command):
        return ' '.join(command)

    def emit_command(self, command):
        return command.split()

    def ingest_entrypoint(self, entrypoint):
        return entrypoint

    def emit_entrypoint(self, entrypoint):
        return [{'key': 'entrypoint', 'value': entrypoint}]

    def ingest_volumes_from(self, volumes_from):
        return volumes_from

    def emit_volumes_from(self, volumes_from):
        return [{'key': 'volumes-from', 'value': vol} for vol in volumes_from]

    def _convert_volume(self, volume):
        """
        This is for ingesting the "volumes" of a app description
        """
        data = {
            'host': volume.get('hostPath'),
            'container': volume.get('containerPath'),
            'readonly': volume.get('mode') == 'RO',
        }
        return data

    def ingest_volumes(self, volumes):
        return [self._convert_volume(volume) for volume in volumes]

    @staticmethod
    def _build_volume(volume):
        """
        Given a generic volume definition, create the volumes element
        """
        return {
            'hostPath': volume.get('host'),
            'containerPath': volume.get('container'),
            'mode': 'RO' if volume.get('readonly') else 'RW'
        }

    def emit_volumes(self, volumes):
        return [
            self._build_volume(volume)
            for volume
            in volumes
        ]

    def ingest_logging(self, logging):
        # Super hacky continued - in self._lookup_parameter() we flatten the logging options
        data = {
            'driver': [p['value'] for p in logging if p['key'] == 'log-driver'][0],
            'options': dict([p['value'].split('=') for p in logging if p['key'] == 'log-opt'])
        }
        return data

    def emit_logging(self, logging):
        output = [{
            'key': 'log-driver',
            'value': logging.get('driver')
        }]
        if logging.get('options') and isinstance(logging.get('options'), dict):
            for k, v in logging.get('options').items():
                output.append({
                    'key': 'log-opt',
                    'value': '{k}={v}'.format(k=k, v=v)
                })
        return output

    def emit_dns(self, dns):
        return [{'key': 'dns', 'value': serv} for serv in dns]

    def emit_domain(self, domain):
        return [{'key': 'dns-search', 'value': d} for d in domain]

    def emit_work_dir(self, work_dir):
        return [{'key': 'workdir', 'value': work_dir}]

    def emit_network(self, network):
        return [{'key': 'net', 'value': net} for net in network]

    def ingest_net_mode(self, net_mode):
        return net_mode.lower()

    def emit_net_mode(self, net_mode):
        return net_mode.upper()

    def emit_user(self, user):
        return [{'key': 'user', 'value': user}]

    def emit_pid(self, pid):
        return [{'key': 'pid', 'value': pid}]

    def emit_env_file(self, env_file):
        return [{'key': 'env-file', 'value': ef} for ef in env_file]

    def emit_expose(self, expose):
        return [{'key': 'expose', 'value': port} for port in expose]

    def emit_labels(self, labels):
        return [{'key': 'label', 'value': label} for label in labels]

    def emit_privileged(self, privileged):
        return [{'key': 'privileged', 'value': privileged}]

    def ingest_fetch(self, fetch):
        return [{'uri': uri} for uri in fetch]

    def emit_fetch(self, fetch):
        return [uri.get('uri') for uri in fetch]
