from unittest import TestCase
import json

from container_transform.fig import FigTransformer


class FigTransformerTests(TestCase):

    def setUp(self):
        """
        Set up transformation classes and associated files here
        """
        self.file_name = './container_transform/tests/fig.yml'
        self.transformer = FigTransformer(self.file_name)

    def test_transform(self):
        t = FigTransformer(self.file_name)
        output = t.transform()

        print(json.dumps(output, indent=4))

    def test_transform_port_mappings(self):
        """
        Test .transform_port_mappings()
        """
        def ecs_port_mapping(host, container):
            return {
                "hostPort": host,
                "containerPort": container
            }

        fig_ports = [
            8000,
            '8000:8000',
            '127.0.0.1:8001:8001',
            '8002:192.168.59.103:8002',
            '127.0.0.1:8003:192.168.59.103:8003'
        ]
        response = self.transformer.transform_port_mappings(port_mappings=fig_ports)

        self.assertListEqual(
            response,
            [
                ecs_port_mapping(8000, 8000),
                ecs_port_mapping(8000, 8000),
                ecs_port_mapping(8001, 8001),
                ecs_port_mapping(8002, 8002),
                ecs_port_mapping(8003, 8003),
            ]
        )

    def test_transform_memory(self):
        """
        Test .transform_memory()
        """
        self.assertEqual(
            self.transformer.transform_memory('5g'),
            5120
        )

        self.assertEqual(
            self.transformer.transform_memory('5m'),
            5
        )

        self.assertEqual(
            self.transformer.transform_memory('5120k'),
            5
        )

        self.assertEqual(
            self.transformer.transform_memory('5242880b'),
            5
        )

        # Test that less than 4mb returns a 4
        self.assertEqual(
            self.transformer.transform_memory('5120b'),
            4
        )

    def test_transform_environment(self):
        """
        Test .transform_environment()
        """
        environment = {'key': 'value'}

        self.assertEqual(
            [{
                'name': 'key',
                'value': 'value'
            }],
            self.transformer.transform_environment(environment)
        )

    def test_transform_command(self):
        """
        Test .transform_command()
        """
        cmd = '/usr/bin/echo hello world'

        self.assertEqual(
            ['/usr/bin/echo', 'hello', 'world'],
            self.transformer.transform_command(cmd)
        )

    def test_transform_entrypoint(self):
        """
        Test .transform_entrypoint()
        """
        cmd = '/usr/bin/echo hello world'

        self.assertEqual(
            ['/usr/bin/echo', 'hello', 'world'],
            self.transformer.transform_entrypoint(cmd)
        )

    def test_convert_container_no_name(self):
        """
        Test .convert_container() without a name
        """
        transformer = FigTransformer(self.file_name)

        container = {
            'build': '.',
            'mem_limit': '2g'
        }

        result = transformer.convert_container(container)

        self.assertEqual(
            {
                'memory': 2048
            },
            result
        )

        self.assertEqual(
            len(transformer.messages),
            1
        )
