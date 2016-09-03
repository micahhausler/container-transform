import json

from copy import deepcopy
from functools import reduce
from collections import Mapping, defaultdict

import yaml

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
    if keys and dic:
        return lookup_nested_dict(dic.get(key, None), *keys)
    if dic:
        return dic.get(key)
    else:
        return None


class KubernetesTransformer(BaseTransformer):
    """
    A transformer for Kubernetes Pods

    TODO: look at http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_pod

    """
    input_type = TransformationTypes.COMPOSE.value

    pod_types = {
        'ReplicaSet': lambda x: x.get('spec').get('template').get('spec'),
        'Deployment': lambda x: x.get('spec').get('template').get('spec'),
        'DaemonSet': lambda x: x.get('spec').get('template').get('spec'),
        'Pod': lambda x: x.get('spec'),
        'ReplicationController': lambda x: x.get('spec').get('template').get('spec')
    }

    def __init__(self, filename=None):
        """
        :param filename: The file to be loaded
        :type filename: str
        """
        obj, stream, volumes_in = {}, None, []
        if filename:
            self._filename = filename
            obj, stream, volumes_in = self._read_file(filename)
        self.obj = obj
        self.stream = stream
        self.volumes_in = volumes_in

        self.volumes = {}

    def _find_convertable_object(self, data):
        """
        Get the first instance of a `self.pod_types`
        """
        data = list(data)
        convertable_object_idxs = [
            idx
            for idx, obj
            in enumerate(data)
            if obj.get('kind') in self.pod_types.keys()
        ]
        if len(convertable_object_idxs) < 1:
            raise Exception("Kubernetes config didn't contain any of {}".format(
                ', '.join(self.pod_types.keys())
            ))
        return list(data)[convertable_object_idxs[0]]

    def _read_stream(self, stream):
        """
        Read in the pod stream
        """
        data = yaml.safe_load_all(stream=stream)
        obj = self._find_convertable_object(data)
        pod = self.pod_types[obj['kind']](obj)
        return obj, pod.get('containers'), self.ingest_volumes_param(pod.get('volumes', []))

    def ingest_volumes_param(self, volumes):
        """
        This is for ingesting the "volumes" of a pod spec
        """
        data = {}
        for volume in volumes:
            if volume.get('hostPath', {}).get('path'):
                data[volume.get('name')] = {
                    'path': volume.get('hostPath', {}).get('path'),
                }
            elif volume.get('emptyDir'):
                data[volume.get('name')] = {}
            else:
                data[volume.get('name')] = {}
            # TODO Support other k8s volume types?
        return data

    def _ingest_volume(self, volume):
        data = {
            'host': self.volumes_in.get(volume.get('name')).get('path', ''),
            'container': volume.get('mountPath', ''),
            'readonly': bool(volume.get('readOnly')),
        }
        return data

    def ingest_volumes(self, volumes):
        return [self._ingest_volume(volume) for volume in volumes]

    def flatten_container(self, container):
        """
        Accepts a kubernetes container and pulls out the nested values into the top level
        """
        for names in ARG_MAP.values():
            if names[TransformationTypes.KUBERNETES.value]['name'] and \
                            '.' in names[TransformationTypes.KUBERNETES.value]['name']:
                kubernetes_dotted_name = names[TransformationTypes.KUBERNETES.value]['name']
                parts = kubernetes_dotted_name.split('.')
                result = lookup_nested_dict(container, *parts)
                if result:
                    container[kubernetes_dotted_name] = result
        return container

    def ingest_containers(self, containers=None):
        containers = containers or self.stream or {}
        # Accept groups api output
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

        output = {
            'kind': 'Deployment',
            'apiVersion': 'extensions/v1beta1',
            'metadata': {
                'name': None,
                'namespace': 'default',
                'labels': {
                    'app': None,
                    'version': 'latest',
                },
            },
            'spec': {
                'replicas': 1,
                'selector': {
                    'matchLabels': {
                        'app': None,
                        'version': 'latest'
                    }
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': None,
                            'version': 'latest'
                        }
                    },
                    'spec': {
                        'containers': json.loads(json.dumps(containers))
                    }
                }
            }
        }
        if self.volumes:
            volumes = sorted(self.volumes.values(), key=lambda x: x.get('name'))
            output['spec']['template']['spec']['volumes'] = volumes

        noalias_dumper = yaml.dumper.SafeDumper
        noalias_dumper.ignore_aliases = lambda self, data: True
        return yaml.dump(
            output,
            default_flow_style=False,
            Dumper=noalias_dumper
        )

    def validate(self, container):
        # Ensure container name
        # container_name = container.get('name', str(uuid.uuid4()))
        # container['name'] = container_name

        container_data = defaultdict(lambda: defaultdict(dict))
        container_data.update(container)

        # Find keys with periods in the name, these are keys that we delete and
        # create the corresponding entry for
        for key, value in deepcopy(container_data).items():
            if key and '.' in key:
                parts = key.split('.')
                data = reduce(lambda x, y: {y: x}, reversed(parts + [value]))
                update_nested_dict(container_data, data)
                del container_data[key]

        return container_data

    @staticmethod
    def _parse_port_mapping(mapping):
        output = {
            'container_port': int(mapping['containerPort']),
            'protocol': mapping.get('protocol', 'TCP').lower(),
        }
        if 'hostPort' in mapping:
            output['host_port'] = int(mapping.get('hostPort'))
        if 'name' in mapping:
            output['name'] = mapping.get('name')
        if 'hostIP' in mapping:
            output['host_ip'] = mapping.get('hostIP')
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

    def emit_port_mappings(self, port_mappings):
        output = []
        for mapping in port_mappings:
            data = {
                'containerPort': mapping['container_port'],
                'protocol': mapping.get('protocol', 'tcp').upper()
            }
            if mapping.get('host_port'):
                data['hostPort'] = mapping['host_port']
            if mapping.get('host_ip'):
                data['hostIP'] = mapping['host_ip']
            if mapping.get('name'):
                data['name'] = mapping['name']
            output.append(data)
        return output

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

        def k(num, thousands):
            return num * thousands

        # if isinstance(memory, int):
        #     # Memory was specified as an integer, meaning it is in bytes
        memory = str(memory)

        bit_shift = {
            'E': {'func': k, 'shift': 10e17},
            'P': {'func': k, 'shift': 10e14},
            'T': {'func': k, 'shift': 10e11},
            'G': {'func': k, 'shift': 10e8},
            'M': {'func': k, 'shift': 10e5},
            'K': {'func': k, 'shift': 10e2},
            'Ei': {'func': lshift, 'shift': 60},
            'Pi': {'func': lshift, 'shift': 50},
            'Ti': {'func': lshift, 'shift': 40},
            'Gi': {'func': lshift, 'shift': 30},
            'Mi': {'func': lshift, 'shift': 20},
            'Ki': {'func': lshift, 'shift': 10},
        }

        if len(memory) > 2 and memory[-2:] in bit_shift.keys():
            unit = memory[-2:]
            number = int(memory[:-2])
            memory = bit_shift[unit]['func'](number, bit_shift[unit]['shift'])
        elif len(memory) > 1 and memory[-1:] in bit_shift.keys():
            unit = memory[-1]
            number = int(memory[:-1])
            memory = bit_shift[unit]['func'](number, bit_shift[unit]['shift'])
        # Cast to a float to properly consume scientific notation
        return int(float(memory))

    def emit_memory(self, memory):
        # return '{mem}Mi'.format(mem=int(memory) >> 20)
        if int(memory) >> 20 > 0:
            return '{mem}Mi'.format(mem=int(memory) >> 20)
        return int(memory)

    def ingest_cpu(self, cpu):
        cpu = str(cpu)
        if cpu[-1] == 'm':
            cpu = float(int(cpu[:-1]) / 1000)
        return float(cpu * 1024)

    def emit_cpu(self, cpu):
        value = float(cpu / 1024)
        if value < 1.0:
            value = '{}m'.format(value * 1000)
        return value

    def ingest_environment(self, environment):
        return dict([(ev['name'], ev.get('value', '')) for ev in environment])

    def emit_environment(self, environment):
        return [{'name': k, 'value': v} for k, v in environment.items()]

    def ingest_command(self, command):
        return ' '.join(command)

    def emit_command(self, command):
        return command.split()

    def ingest_entrypoint(self, entrypoint):
        return ' '.join(entrypoint)

    def emit_entrypoint(self, entrypoint):
        return entrypoint.split()

    @staticmethod
    def _build_volume_name(hostpath):
        return hostpath.replace('/', '-').strip('-')

    def _build_volume(self, volume):
        """
        Given a generic volume definition, create the volumes element
        """
        self.volumes[self._build_volume_name(volume.get('host'))] = {
            'name': self._build_volume_name(volume.get('host')),
            'hostPath': {
                'path': volume.get('host')
            }
        }
        response = {
            'name': self._build_volume_name(volume.get('host')),
            'mountPath': volume.get('container'),

        }
        if volume.get('readonly', False):
            response['readOnly'] = bool(volume.get('readonly', False))
        return response

    def emit_volumes(self, volumes):
        return [
            self._build_volume(volume)
            for volume
            in volumes
        ]
