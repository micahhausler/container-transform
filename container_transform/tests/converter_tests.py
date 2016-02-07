from unittest import TestCase

from container_transform.converter import Converter


class ConverterTests(TestCase):

    def test_ecs_converter(self):
        filename = './container_transform/tests/task.json'
        conv = Converter(filename, 'ecs', 'compose')

        compose_output = conv.convert()

        self.assertIsInstance(compose_output, str)

        self.assertEqual(0, len(conv.messages))

    def test_ecs_converter_just_containers(self):
        filename = './container_transform/tests/containers.json'
        conv = Converter(filename, 'ecs', 'compose')

        compose_output = conv.convert()

        self.assertIsInstance(compose_output, str)

        self.assertEqual(0, len(conv.messages))

    def test_compose_converter_out(self):
        filename = './container_transform/tests/task.json'
        conv = Converter(filename, 'ecs', 'compose')

        compose_output = conv.convert()

        self.assertIsInstance(compose_output, str)

        self.assertEqual(0, len(conv.messages))

    def test_compose_converter_in(self):
        filename = './container_transform/tests/docker-compose.yml'
        conv = Converter(filename, 'compose', 'ecs')

        output = conv.convert()

        self.assertIsInstance(output, str)
