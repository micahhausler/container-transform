from enum import Enum
import logging

LOG = logging.getLogger(__name__)


class TransformationTypes(Enum):
    ECS = 'ecs'
    COMPOSE = 'compose'
    SYSTEMD = 'systemd'


class InputTransformationTypes(Enum):
    ECS = 'ecs'
    COMPOSE = 'compose'


class OutputTransformationTypes(Enum):
    ECS = 'ecs'
    COMPOSE = 'compose'
    SYSTEMD = 'systemd'


ARG_MAP = {
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
    },
    'cpu': {
        TransformationTypes.ECS.value: {
            'name': 'cpu',
            'required': True
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'cpu_shares',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'cpu_shares',
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
            'name': 'mem_limit',
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
    },
    'domain': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'domainname',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': None,
            'required': False
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
    },
    'network': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'net',
            'required': False
        },
        TransformationTypes.SYSTEMD.value: {
            'name': 'net',
            'required': False
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
    },

}
