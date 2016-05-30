from enum import Enum
import logging
from collections import OrderedDict

LOG = logging.getLogger(__name__)


class TransformationTypes(Enum):
    ECS = 'ecs'
    COMPOSE = 'compose'
    SYSTEMD = 'systemd'
    MARATHON = 'marathon'


class InputTransformationTypes(Enum):
    ECS = 'ecs'
    COMPOSE = 'compose'
    MARATHON = 'marathon'


class OutputTransformationTypes(Enum):
    ECS = 'ecs'
    COMPOSE = 'compose'
    SYSTEMD = 'systemd'
    MARATHON = 'marathon'


ARG_MAP = OrderedDict({
    'image': {
        TransformationTypes.ECS.value: {
            'name': 'image',
            'required': True,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'image',
            'required': True,
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'image',
            'required': True,
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.image',
            'required': True,
        },
    },
    'name': {
        TransformationTypes.ECS.value: {
            'name': 'name',
            'required': True,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'name',
            'required': True
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'name',
            'required': True
        },
        TransformationTypes.MARATHON.value: {
            'name': 'id',
            'required': True
        },
    },
    'cpu': {
        TransformationTypes.ECS.value: {
            'name': 'cpu',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'cpu_shares',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'cpu_shares',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'cpus',
            'required': False
        },
    },
    'memory': {
        TransformationTypes.ECS.value: {
            'name': 'memory',
            'required': True
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'mem_limit',
            'required': False,
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'memory',
            'required': False,
        },
        TransformationTypes.MARATHON.value: {
            'name': 'mem',
            'required': False,
        },
    },
    'links': {
        TransformationTypes.ECS.value: {
            'name': 'links',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'links',
            'required': False,
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'links',
            'required': False,
        },
        TransformationTypes.MARATHON.value: {
            'name': 'dependencies',
            'required': False,
        },
    },
    'port_mappings': {
        TransformationTypes.ECS.value: {
            'name': 'portMappings',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'ports',
            'required': False,
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'ports',
            'required': False,
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.portMappings',
            'required': False,
        },
    },
    'environment': {
        TransformationTypes.ECS.value: {
            'name': 'environment',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'environment',
            'required': False,
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'environment',
            'required': False,
        },
        TransformationTypes.MARATHON.value: {
            'name': 'env',
            'required': False,
        },
    },
    'entrypoint': {
        TransformationTypes.ECS.value: {
            'name': 'entryPoint',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'entrypoint',
            'required': False,
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'entrypoint',
            'required': False,
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.parameters.entrypoint',
            'required': False,
        },
    },
    'command': {
        TransformationTypes.ECS.value: {
            'name': 'command',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'command',
            'required': False,
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'command',
            'required': False,
        },
        TransformationTypes.MARATHON.value: {
            'name': 'args',
            'required': False,
        },
    },
    'essential': {
        TransformationTypes.ECS.value: {
            'name': 'essential',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'essential',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': None,
            'required': False
        },
    },
    'volumes_from': {
        TransformationTypes.ECS.value: {
            'name': 'volumesFrom',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'volumes_from',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'volumes_from',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.parameters.volumes-from',
            'required': False,
            'type': list
        },
    },
    'volumes': {
        TransformationTypes.ECS.value: {
            'name': 'mountPoints',
            'attribute': '',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'volumes',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'volumes',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.volumes',
            'required': False
        },
    },
    'dns': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'dns',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'dns',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.parameters.dns',
            'required': False,
            'type': list
        },
    },
    'work_dir': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'working_dir',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'working_dir',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.parameters.workdir',
            'required': False
        },
    },
    'domain': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'dns_search',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.parameters.dns-search',
            'required': False,
            'type': list
        },
    },
    'build': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'build',
            'required': False,
        },
        TransformationTypes.SYSTEMD.value: {
            'name': None,
            'required': False,
        },
        TransformationTypes.MARATHON.value: {
            'name': None,
            'required': False,
        },
    },
    'expose': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'expose',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'expose',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.parameters.expose',
            'required': False,
            'type': list
        },
    },
    'network': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'networks',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'net',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.parameters.net',
            'required': False,
            'type': list
        },
    },
    'net_mode': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'network_mode',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'net',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.network',
            'required': False,
        },
    },
    'privileged': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'privileged',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'privileged',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.privileged',
            'required': False
        },
    },
    'labels': {
        TransformationTypes.ECS.value: {
            'name': 'dockerLabels',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'labels',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'labels',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'labels',
            'required': False
        },
    },
    'logging': {
        TransformationTypes.ECS.value: {
            'name': 'logConfiguration',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'logging',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'logging',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.parameters.log-driver',
            'required': False,
            'type': list,
        },
    },
    'user': {
        TransformationTypes.ECS.value: {
            'name': 'user',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'user',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'user',
            'required': False
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.parameters.user',
            'required': False
        },
    },
    'env_file': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'env_file',
            'required': False,
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'env-file',
            'required': False,
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.parameters.env-file',
            'required': False,
            'type': list,
        },
    },
    'pid': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'pid',
            'required': False,
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'pid',
            'required': False,
        },
        TransformationTypes.MARATHON.value: {
            'name': 'container.docker.parameters.pid',
            'required': False,
        },
    },
})
