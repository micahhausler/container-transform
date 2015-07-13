import click

from .converter import Converter
from .schema import InputTransformationTypes, OutputTransformationTypes
from .version import __version__


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    'input_file',
    default='/dev/stdin',
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
)
@click.option(
    '--input-type',
    'input_type',
    type=click.Choice([v.value.lower() for v in list(InputTransformationTypes)]),
    default=InputTransformationTypes.COMPOSE.value,
)
@click.option(
    '--output-type',
    'output_type',
    type=click.Choice([v.value.lower() for v in list(OutputTransformationTypes)]),
    default=OutputTransformationTypes.ECS.value,
)
@click.option('-v/--no-verbose', default=True, help='Expand/minify json output')
@click.option('-q', default=False, is_flag=True, help='Silence error messages')
@click.version_option(__version__)
def transform(input_file, input_type, output_type, v, q):
    """
    container-transform is a small utility to transform various docker
    container formats to one another.

    Default input type is compose, default output type is ECS

    Default is to read from STDIN if no INPUT_FILE is provided
    """
    converter = Converter(input_file, input_type, output_type)
    output = converter.convert(v)

    click.echo(click.style(output, fg='green'))

    if not q:
        for message in converter.messages:
            click.echo(click.style(message, fg='red', bold=True), err=True)
