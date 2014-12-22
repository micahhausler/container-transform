from enum import Enum
import logging

LOG = logging.getLogger(__name__)


class TransformationTypes(Enum):
    ECS = 'ECS'
    FIG = 'fig'


ARG_MAP = {
    'image': {
        TransformationTypes.ECS.value: 'image',
        TransformationTypes.FIG.value: 'image',
    },
    'name': {
        TransformationTypes.ECS.value: 'name',
        TransformationTypes.FIG.value: None,
    },
    'cpu': {
        TransformationTypes.ECS.value: 'cpu',
        TransformationTypes.FIG.value: None,
    },
    'memory': {
        TransformationTypes.ECS.value: 'memory',
        TransformationTypes.FIG.value: 'mem_limit',
    },
    'links': {
        TransformationTypes.ECS.value: 'links',
        TransformationTypes.FIG.value: 'links',
    },
    'port_mappings': {
        TransformationTypes.ECS.value: 'portMappings',
        TransformationTypes.FIG.value: 'ports',
    },
    'environment': {
        TransformationTypes.ECS.value: 'environment',
        TransformationTypes.FIG.value: 'environment',
    },
    'entrypoint': {
        TransformationTypes.ECS.value: 'entryPoint',
        TransformationTypes.FIG.value: 'entrypoint',
    },
    'command': {
        TransformationTypes.ECS.value: 'command',
        TransformationTypes.FIG.value: 'command',
    },
    'essential': {
        TransformationTypes.ECS.value: 'essential',
        TransformationTypes.FIG.value: None,
    },
    'volumes_from': {
        TransformationTypes.ECS.value: None,
        TransformationTypes.FIG.value: 'volumes_from',
    },
    'dns': {
        TransformationTypes.ECS.value: None,
        TransformationTypes.FIG.value: 'dns',
    },
    'work_dir': {
        TransformationTypes.ECS.value: None,
        TransformationTypes.FIG.value: 'working_dir',
    },
    'domain': {
        TransformationTypes.ECS.value: None,
        TransformationTypes.FIG.value: 'domainname',
    },
    'build': {
        TransformationTypes.ECS.value: None,
        TransformationTypes.FIG.value: 'build'
    },
    'expose': {
        TransformationTypes.ECS.value: None,
        TransformationTypes.FIG.value: 'expose'
    },
    'network': {
        TransformationTypes.ECS.value: None,
        TransformationTypes.FIG.value: 'net'
    },
    'privileged': {
        TransformationTypes.ECS.value: None,
        TransformationTypes.FIG.value: 'privileged'
    },

}
