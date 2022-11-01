import click
import manven
from manven.commands import create_environment, activate_environment, list_environments,\
    remove_environment, deactivate_environment, reset_to_execute, check_first_usage,\
    activate_temp_environment, prune_temp_environments, open_last_environment
from manven.settings import ENVS_PATH, DEFAULT_PKGS

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Command line interface for managing virtual python environments."""
    pass

######################################
# Create the common args and options #
######################################


environment_name_arg = click.argument('environment_name', type=str)

new_op = click.option(
    "--new",
    help="Replace an existing environment with a fresh one.",
    is_flag=True,
)

clone_op = click.option(
    "--clone",
    type=str,
    default=None,
    help="Clone an existing environment instead of creating a fresh one (requires virtualenv-clone).",
)

default_pkgs_op = click.option(
    "-i", "--install",
    type=str,
    default=DEFAULT_PKGS,
    multiple=True,
    help="Install a package in a new environment. Can be specified multiple times. "
         "Overrides what is in the config file.",
)

include_all = click.option(
    "-a",
    "--all",
    help="Whether to include temporary environments",
    is_flag=True,
)


def _get_virtualenv_ops():
    """Returns the options that can be passed to virtualenv"""
    return [
        click.option("-v", "--verbose", is_flag=True, help="Increase verbosity."),
        click.option("-q", "--quiet", is_flag=True, help="Decrease verbosity."),
        click.option("-p", "--python", type=str, default="",
                     help=("The Python interpreter to use, e.g.,\n"
                           "--python=python3.5 will use the python3.5 interpreter\n"
                           "to create the new environment.  The default is the\n"
                           "interpreter that virtualenv was installed with")),
        click.option("--clear", is_flag=True,
                     help="Clear out the non-root install and start from scratch."),
        click.option("--system-site-packages", is_flag=True,
                     help=("Give the virtual environment access to the global\n"
                           "site-packages.\n")),
        click.option("--always-copy", is_flag=True, help="Always copy files rather than symlinking."),
        click.option("--relocatable", is_flag=True,
                     help=("Make an EXISTING virtualenv environment relocatable."
                           "This fixes up scripts and makes all .pth files\n"
                           "relative.")),
        click.option("--no-setuptools", is_flag=True, help="Do not install setuptools in the new virtualenv."),
        click.option("--no-pip", is_flag=True, help="Do not install pip in the new virtualenv."),
        click.option("--no-wheel", is_flag=True, help="Do not install wheel in the new virtualenv."),
        click.option("--extra-search-dir", type=str, default="",
                     help=("Directory to look for setuptools/pip distributions in.\n"
                           "This option can be used multiple times.")),
        click.option("--download", is_flag=True, help="Download preinstalled packages from PyPI."),
        click.option("--no-download", "--never-download", is_flag=True,
                     help="Do not download preinstalled packages from PyPI."),
        click.option("--prompt", is_flag=True, help="Provides an alternative prompt prefix for this environment."),
    ]


def virtualenv_ops(command):
    """Adds all the options from virtualenv to a command."""
    virtualenv_flags = _get_virtualenv_ops()
    for virtualenv_flag in virtualenv_flags:
        command = virtualenv_flag(command)
    return command


###########
# version #
###########

@cli.command()
def version():
    """
    Prints the version of manven.
    """
    print(manven.__version__)


###########
# activate #
###########

@cli.command()
@environment_name_arg
@new_op
@clone_op
@default_pkgs_op
@virtualenv_ops
def activate(
    environment_name,
    *args,
    new=False,
    clone=None,
    install=DEFAULT_PKGS,
    **virtualenv_ops
):
    """
    Activates (and creates if not exists) a virtual environment.
    """
    create_environment(
        environment_name,
        *args,
        replace=new,
        clone=clone,
        default_pkgs=install,
        **virtualenv_ops
    )
    activate_environment(environment_name)


##############
# deactivate #
##############

@cli.command()
def deactivate():
    """
    Deactivates a virtual environment.
    """
    deactivate_environment()


##########
# create #
##########

@cli.command()
@environment_name_arg
@new_op
@clone_op
@default_pkgs_op
@virtualenv_ops
def create(
    environment_name,
    *args,
    new=False,
    clone=None,
    install=DEFAULT_PKGS,
    **virtualenv_ops,
):
    """
    Creates (if not exists) a virtual environment but does not activate it.
    """
    create_environment(
        environment_name,
        *args,
        replace=new,
        clone=clone,
        default_pkgs=install,
        **virtualenv_ops,
    )


##########
# remove #
##########

@cli.command()
@environment_name_arg
def remove(environment_name):
    """
    Removes a virtual environment and deactivates it if it is activated.
    """
    remove_environment(environment_name)


########
# list #
########

@cli.command()
@include_all
def list(all=False):
    """
    Lists all available virtual environments.
    """
    environments = list_environments(include_temporary=all)
    for environment in environments:
        print(environment)


########
# temp #
########

@cli.command()
@default_pkgs_op
@clone_op
@virtualenv_ops
def temp(
    clone=None,
    install=DEFAULT_PKGS,
    **virtualenv_ops
):
    """
    Creates and activates a temporary environment.

    Temporary environments can be pruned with the ``prune`` command.
    """
    activate_temp_environment(
        default_pkgs=install,
        clone=clone,
        **virtualenv_ops
    )


#########
# prune #
#########

@cli.command()
def prune():
    """
    Prunes (removes) all temporary environments.
    """
    prune_temp_environments()


#########
# last #
#########

@cli.command()
def last():
    """
    Opens the last activated environment.
    """
    open_last_environment()


################
# get settings #
################

@cli.group()
def get():
    """
    Returns a setting.
    """


@get.command()
def path():
    """
    Path to where the environments are stored.
    """
    print(ENVS_PATH)


if __name__ == "__main__":
    check_first_usage()
    reset_to_execute()
    cli()
