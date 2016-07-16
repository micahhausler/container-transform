from jinja2 import Template

from .transformer import BaseTransformer


UNIT_TEMPLATE = '''\
# {{ name }}.service #######################################################################
[Unit]
Description={{ name | title }}
After=docker.service {% for link in link_keys %}{{ link }}.service {% endfor %}
Requires=docker.service {% for link in link_keys %}{{ link }}.service {% endfor %}

[Service]
{% if essential == False %}
Type=oneshot {% endif -%}
ExecStartPre=-/usr/bin/docker kill {{ name }}
ExecStartPre=-/usr/bin/docker rm {{ name }}
ExecStartPre=/usr/bin/docker pull {{ image or "<image>" }}
ExecStart=/usr/bin/docker run \\
    --name {{ name }} \\
    {%- if cpu_shares %}
    --cpu {{ cpu_shares }} \\{% endif -%}
    {% if memory %}
    --memory {{ memory }} \\{% endif -%}
    {% if hostname %}
    --hostname {{ hostname }} \\{% endif -%}
    {% if pid %}
    --pid {{ pid }} \\{% endif -%}
    {% if entrypoint %}
    --entrypoint {{ entrypoint }} \\{% endif -%}
    {% for port in ports %}
    -p {{ port }} \\{% endfor -%}
    {% for ep in expose %}
    --expose {{ ep }} \\{% endfor -%}
    {% if net %}
    --net {{ net }} \\{% endif -%}
    {% for volume in volumes %}
    -v {{ volume }} \\{% endfor -%}
    {%- if logging %}
    {% if logging.driver -%}
    --log-driver={{ logging.driver }} \\{% endif -%}
    {% if logging.options %}{% for opt in logging.options|dictsort %}
    --log-opt {{ opt[0] }}={{ opt[1] }} \\{% endfor -%}{% endif %}{% endif -%}
    {% if environment %}{% for env in environment|dictsort %}
    -e "{{ env[0] }}={{ env[1] }}" \\{% endfor -%}{% endif -%}
    {% if labels %}{% for label in labels|dictsort %}
    --label {{ label[0] }}="{{ label[1] }}" \\{% endfor -%}{% endif -%}
    {% for link in links %}
    --link {{ link }} \\{% endfor -%}
    {% for ef in env_file %}
    --env-file {{ ef }} \\{% endfor -%}
    {% for vf in volumes_from %}
    --volumes-from {{ vf }} \\{% endfor -%}
    {% for ns in dns %}
    --dns {{ ns }} \\{% endfor -%}
    {% if work_dir %}
    --workdir {{ work_dir}} \\{% endif -%}
    {% if user %}
    --user {{ user }} \\{% endif -%}
    {% if privileged %}
    --privileged {{ privileged}} \\{%- endif %}
    {{ image or "<image>"  }} {% if command %}\\
    {{ command }}{% endif %}
ExecStop=/usr/bin/docker stop {{ name }}
'''


class SystemdTransformer(BaseTransformer):
    """
    A transformer for docker-compose

    To use this class:

    .. code-block:: python

        transformer = SystemdTransformer()

    """

    def _read_stream(self, stream):
        pass

    def ingest_containers(self, containers=None):
        pass

    def emit_containers(self, containers, verbose=True):
        units = []
        for container in containers:
            link_keys = [link.split(':')[0] for link in container.get('links', [])]
            container['link_keys'] = link_keys
            units.append(Template(UNIT_TEMPLATE).render(container))
        return '\n'.join(units)

    @staticmethod
    def validate(container):
        return container

    def ingest_port_mappings(self, port_mappings):
        pass

    @staticmethod
    def _emit_mapping(mapping):
        parts = []
        if mapping.get('host_ip'):
            parts.append(str(mapping['host_ip']))
        if mapping.get('host_port'):
            parts.append(str(mapping['host_port']))
        if mapping.get('container_ip'):
            parts.append(str(mapping['container_ip']))
        if mapping.get('container_port'):
            parts.append(str(mapping['container_port']))
        output = ':'.join(parts)
        if mapping.get('protocol') == 'udp':
            output += '/udp'
        return output

    def emit_port_mappings(self, port_mappings):
        """
        :param port_mappings: the base schema port_mappings
        :type port_mappings: list of dict
        :return:
        :rtype: list of str
        """
        return [str(self._emit_mapping(mapping)) for mapping in port_mappings]

    def ingest_memory(self, memory):
        pass

    def emit_memory(self, memory):
        return '{}b'.format(memory)

    def ingest_cpu(self, cpu):
        pass

    def emit_cpu(self, cpu):
        return cpu

    def ingest_environment(self, environment):
        pass

    def emit_environment(self, environment):
        return environment

    def ingest_command(self, command):
        pass

    def emit_command(self, command):
        return command

    def ingest_entrypoint(self, entrypoint):
        pass

    def emit_entrypoint(self, entrypoint):
        return entrypoint

    def ingest_volumes_from(self, volumes_from):
        pass

    def emit_volumes_from(self, volumes_from):
        return volumes_from

    def ingest_volumes(self, volumes):
        pass

    @staticmethod
    def _emit_volume(volume):
        volume_str = volume.get('host') + ':' + volume.get('container', ':')
        volume_str = volume_str.strip(':')

        if volume.get('readonly') and len(volume_str):
            volume_str += ':ro'
        return volume_str

    def emit_volumes(self, volumes):
        return [
            self._emit_volume(volume)
            for volume
            in volumes
            if len(self._emit_volume(volume))
        ]

    def ingest_labels(self, labels):
        pass

    def emit_labels(self, labels):
        return labels

    def ingest_logging(self, logging):
        pass

    def emit_logging(self, logging):
        return logging
