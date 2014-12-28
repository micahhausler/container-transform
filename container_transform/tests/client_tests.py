from unittest import TestCase, skip
import json


from click.testing import CliRunner

from container_transform.client import transform


@skip
class ClientTests(TestCase):
    """
    Tests for client
    """
    def setUp(self):
        self.fig_input = (
            '\n'
            'web:\n'
            '  image: me/myapp\n'
            '  mem_limit: 1024b\n'
            '\n'
            'web2:\n'
            '  build: .\n'
            '  mem_limit: 1024b\n'
        )

    def test_prompt_fig_quiet(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('fig.yml', 'w') as f:
                f.write(self.fig_input)

            result = runner.invoke(transform, ['fig.yml', '-q'])
            assert result.exit_code == 0

            data = json.loads(result.output)

            self.assertIn(
                {
                    'name': 'web',
                    'image': 'me/myapp',
                    'memory': 4,
                    'essential': True
                },
                data,
            )
            self.assertIn(
                {
                    'name': 'web2',
                    'memory': 4,
                    'essential': True
                },
                data,
            )

    def test_prompt_fig_no_verbose(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('fig.yml', 'w') as f:
                f.write(self.fig_input)

            result = runner.invoke(transform, ['fig.yml'])
            assert result.exit_code == 0

            data = []
            messages = set()

            for line in result.output.split('\n'):
                try:
                    data = json.loads(line)
                except ValueError:
                    if bool(line):
                        messages.add(line)

            self.assertIn(
                {
                    'name': 'web',
                    'image': 'me/myapp',
                    'memory': 4,
                    'essential': True
                },
                data,
            )
            self.assertIn(
                {
                    'name': 'web2',
                    'memory': 4,
                    'essential': True
                },
                data,
            )

            self.assertEqual(
                len(messages),
                1
            )

    def test_prompt_fig_verbose(self):

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('fig.yml', 'w') as f:
                f.write(self.fig_input)

            result = runner.invoke(transform, ['fig.yml', '-v'])
            assert result.exit_code == 0

            lines = result.output.split('\n')

            data = json.loads(''.join(lines[:-2]))

            message = lines[-2]

            self.assertIn(
                {
                    'name': 'web',
                    'image': 'me/myapp',
                    'memory': 4,
                    'essential': True
                },
                data,
            )
            self.assertIn(
                {
                    'name': 'web2',
                    'memory': 4,
                    'essential': True
                },
                data,
            )

            self.assertEqual(
                str(message),
                (
                    "The output type ECS does not support the parameter 'build'. "
                    "The parameter 'build': '.' will be ignored for container web2."
                )
            )
