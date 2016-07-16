import json
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
        output_dict = json.loads(output)

        # NOTE: We can't just check an output file because it appears the
        # environment dictionary is being serialized in a non-deterministic
        # order.  TODO: Fix that.
        for definition in output_dict['containerDefinitions']:
            if definition['name'] == 'web4':
                # Check read only volumes definition
                volumesFrom = definition['volumesFrom']
                self.assertIn({'sourceContainer': 'web3', 'readOnly': True}, volumesFrom)
                self.assertIn({'sourceContainer': 'logs'}, volumesFrom)

        self.assertIsInstance(output, str)

    def test_compose_converter_v2_to_ecs(self):
        self.maxDiff = None

        filename = './container_transform/tests/composev2_extended.yml'
        output_filename = './container_transform/tests/composev2_extended_output.json'
        conv = Converter(filename, 'compose', 'ecs')

        output = conv.convert()
        output_dict = json.loads(output)

        output_want = json.load(open(output_filename, 'r'))
        self.assertDictEqual(output_dict, output_want)

    def test_compose_converter_v2_systemd(self):
        self.maxDiff = None

        filename = './container_transform/tests/composev2.yml'
        output_filename = './container_transform/tests/composev2_output.service'
        conv = Converter(filename, 'compose', 'systemd')

        output = conv.convert()

        output_want = open(output_filename, 'r').read()
        self.assertEqual(output, output_want)

    def test_compose_converter_v2_0(self):
        self.maxDiff = None

        filename = './container_transform/tests/composev2.0.yml'
        output_filename = './container_transform/tests/composev2.0_output.service'
        conv = Converter(filename, 'compose', 'systemd')

        output = conv.convert()

        output_want = open(output_filename, 'r').read()
        self.assertEqual(output, output_want)
