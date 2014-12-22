import json

import click

from .fig import FigTransformer
from .schema import TransformationTypes
from .version import __version__


TRANSFORMER_CLASSES = {
    TransformationTypes.FIG.value: FigTransformer
}
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
    type=click.Choice(['fig']),
    default=TransformationTypes.FIG.value,
)
@click.option(
    '--output-type',
    'output_type',
    type=click.Choice(['ECS']),
    default=TransformationTypes.ECS.value,
)
@click.option('-v/--no-verbose', default=False, help='Expand json output')
@click.option('-q', default=False, is_flag=True, help='Silence error messages')
@click.version_option(__version__)
def transform(input_file, input_type, output_type, v, q):
    """
    Transform is a small utility to transform various docker container formats to one another.

    Currently only input type is Fig and output type is EC2 Container Service

    Default is to read from STDIN if no INPUT_FILE is provided
    """
    transformer = TRANSFORMER_CLASSES[input_type](input_file, output_type=output_type)
    output = transformer.transform()

    if v:
        click.echo(click.style(json.dumps(output, indent=4), fg='green'))
    else:
        click.echo(click.style(json.dumps(output), fg='green'), )

    if not q:
        for message in transformer.messages:
            click.echo(click.style(message, fg='red', bold=True), err=True)
