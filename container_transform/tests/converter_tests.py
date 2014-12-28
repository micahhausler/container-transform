from unittest import TestCase

from container_transform.converter import Converter


class ConverterTests(TestCase):

    def test_converter(self):

        filename = './container_transform/tests/fig.yml'
        conv = Converter(filename, 'fig', 'ecs')

        output = conv.convert()

        self.assertIsInstance(output, str)
