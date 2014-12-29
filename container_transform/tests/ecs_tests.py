from unittest import TestCase

from mock import patch
import uuid

from container_transform.ecs import ECSTransformer


class ECSTransformerTests(TestCase):
    """
    Tests for ECS Transformer
    """

    def setUp(self):
        self.file_name = './container_transform/tests/task.json'
        self.transformer = ECSTransformer(self.file_name)

    @patch.object(uuid, 'uuid4', return_value='2e9c3538-b9d3-4f47-8a23-2a19315b370b')
    def test_validate(self, mock_uuid):
        """
        Test .validate()
        """
        container = {
            'image': 'postgres:9.3',
            'cpu': 200,
            'memory': 40
        }

        validated = self.transformer.validate(container)
        self.assertEqual(
            validated['name'],
            mock_uuid.return_value
        )
        self.assertTrue(validated['essential'])

    def test_ingest_cpu(self):
        cpu = 100
        self.assertEqual(
            self.transformer.ingest_cpu(cpu),
            cpu
        )

    def test_emit_cpu(self):
        cpu = 100
        self.assertEqual(
            self.transformer.emit_cpu(cpu),
            cpu
        )
