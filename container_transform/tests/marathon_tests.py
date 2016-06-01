from unittest import TestCase

from container_transform.marathon import MarathonTransformer


class MarathonTransformerTests(TestCase):
    """
    Tests for the MarathonTransformer
    """

    def setUp(self):
        self.file_name = './container_transform/tests/marathon-test.json'
        self.transformer = MarathonTransformer(self.file_name)

    def test_emit_fetch(self):
        fetch = [
            {'uri': 'https://s3.amazonaws.com/bucket/item.json'},
            {'uri': 'hdfs://hdfs.marathon.mesos/path/item.json'}
        ]
        self.assertEqual(
            self.transformer.emit_fetch(fetch),
            [
                {'uri': 'https://s3.amazonaws.com/bucket/item.json'},
                {'uri': 'hdfs://hdfs.marathon.mesos/path/item.json'}
            ]
        )
