from unittest import TestCase

from container_transform.chronos import ChronosTransformer


class ChronosTransformerTests(TestCase):
    """
    Tests for the ChronosTransformer
    """

    def setUp(self):
        self.file_name = './container_transform/tests/fixtures/chronos.json'
        self.transformer = ChronosTransformer(self.file_name)

    def test_validate(self):
        """
        Test .validate()
        """
        container = {
            'image': 'ubuntu:16.04',
            'cpu': 200,
            'memory': 40,
            'name': 'report_task'
        }

        validated = self.transformer.validate(container)
        self.assertEqual(
            validated['name'],
            'report_task'
        )

    def test_ingest_cpu(self):
        cpu = 0.5
        self.assertEqual(
            self.transformer.ingest_cpu(cpu),
            512
        )

    def test_emit_cpu(self):
        cpu = 512
        self.assertEqual(
            self.transformer.emit_cpu(cpu),
            0.5
        )

    def test_ingest_environment(self):
        environment = [
            {'name': 'CT_INPUT_TYPE', 'value': 'compose'},
            {'name': 'CT_OUTPUT_TYPE', 'value': 'chronos'},
        ]
        self.assertEqual(
            self.transformer.ingest_environment(environment),
            {
                'CT_INPUT_TYPE': 'compose',
                'CT_OUTPUT_TYPE': 'chronos',
            }
        )

    def test_emit_environment(self):
        environment = {
            'CT_INPUT_TYPE': 'compose',
            'CT_OUTPUT_TYPE': 'chronos',
        }
        self.assertEqual(
            self.transformer.emit_environment(environment),
            [
                {'name': 'CT_INPUT_TYPE', 'value': 'compose'},
                {'name': 'CT_OUTPUT_TYPE', 'value': 'chronos'},
            ]
        )

    def test_emit_port_mapping(self):
        mappings = [
            {'container_port': 5432, 'host_port': 5432},
            {'container_port': 3000},
            {'container_port': 53, 'protocol': 'udp'},
        ]
        self.assertEqual(
            self.transformer.emit_port_mappings(mappings),
            [
                {'key': 'publish', 'value': '5432:5432'},
                {'key': 'publish', 'value': '3000'},
                {'key': 'publish', 'value': '53/udp'},
            ]
        )
