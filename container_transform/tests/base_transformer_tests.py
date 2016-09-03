from unittest import TestCase

from container_transform.transformer import BaseTransformer
from container_transform.schema import ARG_MAP


class BaseTransformerTests(TestCase):
    """
    Tests for the BaseTransformer class
    """

    def test_base_transformer_has_all_methods(self):
        """
        Test to confirm that the BaseTransformer has methods (abstract or
        otherwise) for each possible parameter (except for ``build`` and
        ``essential``).
        """

        available_params = set(ARG_MAP.keys())

        emit_methods = set([a[5:] for a in dir(BaseTransformer) if a.startswith('emit_')])
        ingest_methods = set([a[7:] for a in dir(BaseTransformer) if a.startswith('ingest_')])

        self.assertEqual(
            available_params.difference(emit_methods),
            {'build', 'essential', 'volumes_from', 'logging'}
        )

        self.assertEqual(
            available_params.difference(ingest_methods),
            {'build', 'essential', 'volumes_from', 'logging'}
        )
