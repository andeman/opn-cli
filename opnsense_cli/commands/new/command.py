import click
import os

from opnsense_cli.facades.code_generator.click_command_facade import ClickCommandFacadeCodeGenerator
from opnsense_cli.parser.opnsense_model import OpnsenseModelParser
from opnsense_cli.factories.code_generator.click_option import ClickOptionCodeFactory
from opnsense_cli.facades.code_generator.click_command import ClickCommandCodeGenerator
from opnsense_cli.facades.template_engines.jinja2 import Jinja2TemplateEngine


@click.group()
def command(**kwargs):
    """
    Generate code for a new command
    """


@command.command()
@click.argument('click_group')
@click.argument('click_command')
@click.option(
    '--url', '-u',
    help=(
        'The url to the model xml. For core unbound e.g. https://raw.githubusercontent.com'
        '/opnsense/core/master/src/opnsense/mvc/app/models/OPNsense/Unbound/Unbound.xml'
    ),
    show_default=True,
    required=True
)
@click.option(
    '--tag', '-t',
    help='The xml tag from the model.xml e.g. dnsbl for unbound dnsbl command',
    show_default=True,
    required=True
)
@click.option(
    '--template-basedir', '-tb',
    help='The template basedir path',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../../../opnsense_cli/templates')
)
@click.option(
    '--template-command', '-tc',
    help='The template for the command relative to the template basedir.',
    show_default=True,
    default='code_generator/command/command.py.j2'
)
@click.option(
    '--template-facade', '-tf',
    help='The template for the command relative to the template basedir.',
    show_default=True,
    default='code_generator/command/facade.py.j2'
)
@click.option(
    '--command-output-dir', '-cod',
    help='The output directory for the generated command',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../../../output/commands/plugin'),
)
@click.option(
    '--facade-output-dir', '-fod',
    help='The output directory for the generated facade',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../../../output/facades/command/plugin'),
)
def core(**kwargs):
    """
    Generate new command code for a core module.

    For a list of core modules see:

    https://docs.opnsense.org/development/api.html#core-api

    Search model.xml files here:

    https://github.com/opnsense/core/tree/master/src/opnsense/mvc/app/models/OPNsense

    Example:

    $ opn-cli new command core unbound dnsbl --tag dnsbl \

    --url https://raw.githubusercontent.com/opnsense/core/master/src/opnsense/mvc/app/models/OPNsense/Unbound/Unbound.xml
    """
    generate_command_files('plugin', **kwargs)


@command.command()
@click.argument('click_group')
@click.argument('click_command')
@click.option(
    '--url', '-u',
    help=(
        'The url to the model xml. For net/haproxy e.g. https://raw.githubusercontent.com/opnsense/plugins/blob/master/'
        'net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml'),
    show_default=True,
    required=True
)
@click.option(
    '--tag', '-t',
    help='The xml tag from the model.xml e.g. servers for haproxy backend server command',
    show_default=True,
    required=True
)
@click.option(
    '--template-basedir', '-tb',
    help='The template basedir path',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../../../opnsense_cli/templates')
)
@click.option(
    '--template-command', '-tc',
    help='The template for the command relative to the template basedir.',
    show_default=True,
    default='code_generator/command/command.py.j2'
)
@click.option(
    '--template-facade', '-tf',
    help='The template for the command relative to the template basedir.',
    show_default=True,
    default='code_generator/command/facade.py.j2'
)
@click.option(
    '--command-output-dir', '-cod',
    help='The output directory for the generated command',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../../../output/commands/plugin'),
)
@click.option(
    '--facade-output-dir', '-fod',
    help='The output directory for the generated facade',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../../../output/facades/command/plugin'),
)
def plugin(**kwargs):
    """
    Generate new command code for a plugin module.

    For a list of plugin modules see:

    https://docs.opnsense.org/development/api.html#plugins-api

    Search for model.xml under this url:

    https://github.com/opnsense/plugins

    Example:

    $ opn-cli new command plugin haproxy server --tag servers \
    --url https://raw.githubusercontent.com/opnsense/plugins/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/
    HAProxy/HAProxy.xml

    """
    generate_command_files('plugin', **kwargs)


def generate_command_files(model_type, **kwargs):
    parser = OpnsenseModelParser(kwargs['url'], kwargs['tag'])
    template_engine = Jinja2TemplateEngine(kwargs['template_basedir'])
    option_factory = ClickOptionCodeFactory()

    command_code_generator = ClickCommandCodeGenerator(
        parser,
        template_engine,
        option_factory,
        kwargs['template_command'],
        kwargs['click_group'],
        kwargs['click_command'],
        kwargs['tag'],
        model_type,
    )

    command_facade_generator = ClickCommandFacadeCodeGenerator(
        parser,
        template_engine,
        option_factory,
        kwargs['template_facade'],
        kwargs['click_group'],
        kwargs['click_command'],
        kwargs['tag'],
        model_type,
    )

    click.echo(command_code_generator.write_code(kwargs['command_output_dir']))
    click.echo(command_facade_generator.write_code(kwargs['facade_output_dir']))


if __name__ == '__main__':
    command()
