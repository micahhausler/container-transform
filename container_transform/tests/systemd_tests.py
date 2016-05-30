import os
from unittest import TestCase


from container_transform.systemd import SystemdTransformer


class SystemdTransformerTests(TestCase):

    def setUp(self):
        self.file_name = './container_transform/tests/docker-compose.yml'
        self.transformer = SystemdTransformer()

    def test_emit_containers(self):
        containers = [{
            'command': 'celery worker',
            'environment': {
                'AWS_ACCESS_KEY_ID': 'AAAAAAAAAAAAAAAAAAAA',
                'AWS_EC2_REGION': 'us-east-1',
                'AWS_SECRET_ACCESS_KEY': '1111111111111111111111111111111111111111',
                'BROKER_URL': 'redis://redis:6379/0',
                'DB_HOST': 'db',
                'DB_NAME': 'postgres',
                'DB_PAS': 'postgres',
                'DB_USER': 'postgres'
            },
            'image': 'me/myapp',
            'links': ['db', 'redis', 'web'],
            'memory': '67108864b',
            'name': 'worker',
            'ports': [
                '8000',
                '8000:8000',
                '127.0.0.1:8001:8001',
                '8002:192.168.59.103:8002',
                '127.0.0.1:8003:192.168.59.103:8003'
            ],
            'labels': {
                'com.example.foo': 'bar',
                'com.example.bar': None
            },
            'logging': {
                'driver': 'gelf',
                'options': {
                    'tag': 'worker',
                    'gelf-address': 'udp://127.0.0.1:12900'
                }
            }
        }]
        service_file = '{}/worker.service'.format(os.path.dirname(__file__))
        service_contents = open(service_file).read()
        self.assertEqual(
            self.transformer.emit_containers(containers),
            service_contents
        )

    def test_ingest_methods(self):
        """
        Test that "ingest_*" methods return nothing
        """
        for attribute in dir(self.transformer):
            if str(attribute).startswith('ingest_'):
                method = getattr(self.transformer, attribute)
                self.assertIsNone(method(None))

        self.assertIsNone(self.transformer._read_stream(''))

    def test_emit_unchanged(self):

        # .validate()
        self.assertEqual(self.transformer.validate('hi'), 'hi')

        # .emit_cpu()
        self.assertEqual(self.transformer.emit_cpu('1'), '1')

        # .emit_environment()
        self.assertEqual(self.transformer.emit_environment([{}]), [{}])

        # .emit_command()
        self.assertEqual(self.transformer.emit_command('/bin/true'), '/bin/true')

        # .emit_entrypoint()
        self.assertEqual(self.transformer.emit_entrypoint('/bin/true'), '/bin/true')

        # .emit_volumes_from()
        self.assertEqual(self.transformer.emit_volumes_from(['web']), ['web'])

    def test_emit_memory(self):
        self.assertEqual(self.transformer.emit_memory('1024'), '1024b')

    def test_emit_environment(self):
        self.assertEqual(self.transformer.emit_memory('1024'), '1024b')

    def test_emit_volumes(self):
        volumes = [
            {'host': '/path', 'container': '/path', 'readonly': True},
            {'host': '/path', 'container': '/path', 'readonly': False}
        ]

        expected_output = [
            '/path:/path:ro',
            '/path:/path'
        ]

        self.assertEqual(
            self.transformer.emit_volumes(volumes),
            expected_output
        )

    def test_emit_mapping(self):
        """
        Test ._emit_mapping()
        """
        mappping = {
            'host_ip': '192.168.59.103',
            'host_port': 8000,
            'container_ip': '127.0.0.1',
            'container_port': 80,
        }

        self.assertEqual(
            self.transformer._emit_mapping(mappping),
            '192.168.59.103:8000:127.0.0.1:80'
        )

    def test_emit_mapping_missing_ports(self):
        """
        Test ._emit_mapping() missing ports
        """
        mapping = {
            'host_ip': '192.168.59.103',
            'container_ip': '127.0.0.1',
        }

        self.assertEqual(
            self.transformer._emit_mapping(mapping),
            '192.168.59.103:127.0.0.1'
        )
