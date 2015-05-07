from enum import Enum
import logging

LOG = logging.getLogger(__name__)


class TransformationTypes(Enum):
    ECS = 'ecs'
    FIG = 'fig'
    COMPOSE = 'compose'


ARG_MAP = {
    'image': {
        TransformationTypes.ECS.value: {
            'name': 'image',
            'required': True,
        },
        TransformationTypes.FIG.value: {
            'name': 'image',
            'required': True,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'image',
            'required': True,
        },
    },
    'name': {
        TransformationTypes.ECS.value: {
            'name': 'name',
            'required': True,
        },
        TransformationTypes.FIG.value: {
            'name': 'name',
            'required': True
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'name',
            'required': True
        },
    },
    'cpu': {
        TransformationTypes.ECS.value: {
            'name': 'cpu',
            'required': True
        },
        TransformationTypes.FIG.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'cpu_shares',
            'required': False
        },
    },
    'memory': {
        TransformationTypes.ECS.value: {
            'name': 'memory',
            'required': True
        },
        TransformationTypes.FIG.value: {
            'name': 'mem_limit',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'mem_limit',
            'required': False,
        },
    },
    'links': {
        TransformationTypes.ECS.value: {
            'name': 'links',
            'required': False,
        },
        TransformationTypes.FIG.value: {
            'name': 'links',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'links',
            'required': False,
        },
    },
    'port_mappings': {
        TransformationTypes.ECS.value: {
            'name': 'portMappings',
            'required': False,
        },
        TransformationTypes.FIG.value: {
            'name': 'ports',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'ports',
            'required': False,
        },
    },
    'environment': {
        TransformationTypes.ECS.value: {
            'name': 'environment',
            'required': False,
        },
        TransformationTypes.FIG.value: {
            'name': 'environment',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'environment',
            'required': False,
        },
    },
    'entrypoint': {
        TransformationTypes.ECS.value: {
            'name': 'entryPoint',
            'required': False,
        },
        TransformationTypes.FIG.value: {
            'name': 'entrypoint',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'entrypoint',
            'required': False,
        },
    },
    'command': {
        TransformationTypes.ECS.value: {
            'name': 'command',
            'required': False,
        },
        TransformationTypes.FIG.value: {
            'name': 'command',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'command',
            'required': False,
        },
    },
    'essential': {
        TransformationTypes.ECS.value: {
            'name': 'essential',
            'required': False
        },
        TransformationTypes.FIG.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': None,
            'required': False
        },
    },
    'volumes_from': {
        TransformationTypes.ECS.value: {
            'name': 'volumesFrom',
            'required': False
        },
        TransformationTypes.FIG.value: {
            'name': 'volumes_from',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
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
        TransformationTypes.FIG.value: {
            'name': 'volumes',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'volumes',
            'required': False
        }
    },
    'dns': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.FIG.value: {
            'name': 'dns',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'dns',
            'required': False
        },
    },
    'work_dir': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.FIG.value: {
            'name': 'working_dir',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'working_dir',
            'required': False
        },
    },
    'domain': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.FIG.value: {
            'name': 'domainname',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'domainname',
            'required': False
        },
    },
    'build': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.FIG.value: {
            'name': 'build',
            'required': False,
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'build',
            'required': False,
        },
    },
    'expose': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.FIG.value: {
            'name': 'expose',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'expose',
            'required': False
        },
    },
    'network': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.FIG.value: {
            'name': 'net',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'net',
            'required': False
        },
    },
    'privileged': {
        TransformationTypes.ECS.value: {
            'name': None,
            'required': False
        },
        TransformationTypes.FIG.value: {
            'name': 'privileged',
            'required': False
        },
        TransformationTypes.COMPOSE.value: {
            'name': 'privileged',
            'required': False
        },
    },

}
