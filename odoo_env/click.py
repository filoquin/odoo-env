import os
import click
from odoo_env.config import OeConfig
from odoo_env.odooenv import OdooEnv
from odoo_env.messages import Msg
from .__init__ import __version__


def execute(commands):
    for command in commands:
        if command and command.check():
            if command.usr_msg:
                click.echo(Msg().inf(command.usr_msg))
            command.execute()

def common_work(prod, debug, nginx, c, no_repos=False, v=False, backup_file=False):
    client = c.strip() if c else False

    # obtener el cliente
    if client:
        OeConfig().save_client(client)
    client = OeConfig().get_client()
    if not client:
        click.echo(Msg().err('Project name not known, please issue -c option'))

    # obtener ambiente
    if prod:
        OeConfig().save_environment('prod')
    if debug:
        OeConfig().save_environment('debug')

    # crear las opciones
    _options = {
        'verbose': v,
        'debug': OeConfig().get_environment() == 'debug',
        'no-repos': no_repos,
        'nginx': nginx,
        'backup_file': backup_file,
    }
    mode = 'Production' if OeConfig().get_environment() == 'prod' else 'Development'

    return _options, mode, client

CONTEXT_SETTINGS = dict(help_option_names=['-h'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Odoo Environment by jeo Software <jorge.obiols@gmail.com>."""

# INSTALL----------------------------------------------------------------------

@cli.command('install')
@click.option('--prod', is_flag=True, help='Set the production environment (persistent setting)')
@click.option('--debug', is_flag=True, help='Set the development environment (persistent setting)')
@click.option('--nginx', is_flag=True, help='Install nginx reverse proxy')
@click.option('-c', help='Set the Proyect code name (persistent setting)')
@click.option('--no-repos', is_flag=True, help='Does not clone or pull the project repositories')
@click.option('-v', is_flag=True, help='Verbose mode')
def install(prod, debug, nginx, c, no_repos, v):
    """Install / Upgrade Odoo in Development or Production. See oe help install"""
    options, mode, client = common_work(prod, debug, nginx, c, no_repos, v)
    click.echo(Msg().inf('Installing / Updating %s in %s mode\n' % (client, mode)))
    commands = OdooEnv(options).install(client)
    execute(commands)

# CONFIG ------------------------------------------------------------------

@cli.command('config')
@click.option('--prod', is_flag=True, help='Set the production environment (persistent setting)')
@click.option('--debug', is_flag=True, help='Set the development environment (persistent setting)')
@click.option('-c', help='Set the Proyect code name (persistent setting)')
@click.option('-v', is_flag=True, help='Verbose mode')
def config(prod, debug, c, v):
    """Create / Update odoo.conf file acording to Project."""
    no_repos = nginx = False
    options, mode, client = common_work(prod, debug, nginx, c, no_repos, v)
    click.echo('writing odoo.conf for project %s in %s mode' % (client, mode))
    commands = OdooEnv(options).write_config(client)
    execute(commands)

# UP --------------------------------------------------------------------

@cli.command('up')
@click.option('--prod', is_flag=True, help='Set the production environment. (persistent setting)')
@click.option('--debug', is_flag=True, help='Set the development environment. (persistent setting)')
@click.option('--nginx', is_flag=True, help='Start nginx reverse proxy.')
@click.option('--env', is_flag=True, help='Start only companion containers.')
@click.option('-c', help='Set the Proyect code name. (persistent setting)')
@click.option('-v', is_flag=True, help='Verbose mode.')
@click.option('-d', help='Database name. (defaults to projectname_prod')
def up(prod, debug, nginx, env, c, v):
    """Start odoo container."""

    click.echo('Starging containers')

# PULL -----------------------------------------------------------------------

@cli.command('pull')
def pull():
    """Pull Docker images."""
    click.echo('Downloading images...')

# DOWN ------------------------------------------------------------------------

@cli.command("down")
@click.option('-all', is_flag=True, help='Stop all containers, not only odoo')
def down(all):
    """Stop odoo containers."""
    click.echo('System is going down...')

# UPDATE ------------------------------------------------------------------------

@cli.command("update")
@click.option('-m', default='all', help='Module to update, or list of modules. Defaults to all')
@click.option('-d', help='Database name. (defaults to projectname_prod)')
def update(m, d):
    """Update database module, list of modules or all modules."""
    click.echo('System is going down...')

# DATABASE --------------------------------------------------------------------

@cli.group('db')
def db():
    """Database operations."""

@db.command('backup')
@click.option('-c', help='Set the Proyect code name. (persistent setting)')
@click.option('-d', help='Database name. (defaults to projectname_prod')
@click.option('--prod', is_flag=True, help='Set the production environment. (persistent setting)')
@click.option('--debug', is_flag=True, help='Set the development environment. (persistent setting)')
def _backup_database(c, d, prod, debug):
    """Backup current database to default location."""
    click.echo('Backing up database...')

@db.command('restore')
@click.option('-c', help='Set the Proyect code name. (persistent setting)')
@click.option('-d', help='Database name. (defaults to projectname_prod')
@click.option('--prod', is_flag=True, help='Set the production environment. (persistent setting)')
@click.option('--debug', is_flag=True, help='Set the development environment. (persistent setting)')
@click.option('-f', help='Filename to restore, defaults to newest backup file')
def _restore_database(c, d, prod, debug, f):
    """Restore backup from default location / production location."""
    click.echo('Restoring database from local...')

@db.command('list')
def _list():
    """List backup files from local filesystem."""
    click.echo('list database backups')

# VERSION ---------------------------------------------------------------------

@cli.command('version')
def version():
    """Show version information."""
    click.echo('oe version %s' % __version__)

# HELP-------------------------------------------------------------------------

@cli.group('help')
def help():
    """Get help on a command."""

def _show_help(command):
    try:
        data_dir = os.path.join(os.path.dirname(__file__))
        with open(data_dir + '/doc/%s.hlp' % command, 'r') as f:
            help = f.read()
        click.echo_via_pager(help)
    except FileNotFoundError as e:
        click.echo(e)

@help.command('install')
def _help_config():
    _show_help('install')

@help.command('up')
def _help_up():
    _show_help('up')

@help.command('down')
def _help_down():
    _show_help('down')

@help.command('backup')
def _help_backup():
    _show_help('backup')

@help.command('restore')
def _help_restore():
    _show_help('restore')

@help.command('config')
def _help_config():
    _show_help('config')

# SERVER HELP-------------------------------------------------------------------------

@cli.command('server-help')
def server_help():
    """Get server help."""
    click.echo('showing server help')

# OPTIONS-------------------------------------------------------------------------

@cli.command('options')
@click.option('-c', help='Set the Proyect code name. (persistent setting)')
@click.option('--prod', is_flag=True, help='Set the production environment. (persistent setting)')
@click.option('--debug', is_flag=True, help='Set the development environment. (persistent setting)')
def _options(c, prod, debug):
    """Show / Change options."""
    client = c.split() if c else OeConfig().get_client()
    if prod and debug:
        click.echo(Msg().err('Environment must be prod or debug not both.'))
    if client:
        OeConfig().save_client(client)
    if prod:
        OeConfig().save_environment('prod')
    if debug:
        OeConfig().save_environment('debug')

    client = OeConfig().get_client()
    client_path = OeConfig().get_client_path(client)
    environment = OeConfig().get_environment()

    click.echo(Msg().inf('Project %s' % client))
    click.echo(Msg().inf('Project path %s' % client_path))
    click.echo(Msg().inf('Environment %s' % environment))



if __name__ == '__main__':
    cli()
