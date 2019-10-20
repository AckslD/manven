import click
import manven
from manven.commands import create_environment, activate_environment, list_environments,\
    remove_environment, deactivate_environment, reset_to_execute, check_first_usage,\
    activate_temp_environment, prune_temp_environments
from manven.settings import ENVS_PATH

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Command line interface for managing virtual python environments."""
    pass


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
@click.argument('environment_name', type=str)
@click.option(
    "--new",
    help="Replace an existing environment with a fresh one.",
    is_flag=True,
)
@click.option(
    "--no-manven",
    help="Don't install manven in the new environment.",
    is_flag=True,
)
def activate(environment_name, new=False, no_manven=False):
    """
    Activates (and creates if not exists) a virtual environment.
    """
    create_environment(environment_name, replace=new, no_manven=no_manven)
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
@click.argument('environment_name', type=str)
@click.option(
    "--new",
    help="Replace an existing environment with a fresh one.",
    is_flag=True,
)
@click.option(
    "--no-manven",
    help="Don't install manven in the new environment.",
    is_flag=True,
)
def create(environment_name, new=False, no_manven=False):
    """
    Creates (if not exists) a virtual environment but does not activate it.
    """
    create_environment(environment_name, replace=new, no_manven=no_manven)


##########
# remove #
##########

@cli.command()
@click.argument('environment_name', type=str)
def remove(environment_name):
    """
    Removes a virtual environment and deactivates it if it is activated.
    """
    remove_environment(environment_name)


########
# list #
########

@cli.command()
@click.option(
    "-a",
    "--all",
    help="Whether to include temporary environments",
    is_flag=True,
)
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
@click.option(
    "--no-manven",
    help="Don't install manven in the new environment.",
    is_flag=True,
)
def temp(no_manven=False):
    """
    Creates and activates a temporary environment.

    Temporary environments can be pruned with the ``prune`` command.
    """
    activate_temp_environment(no_manven=no_manven)


#########
# prune #
#########

@cli.command()
def prune():
    """
    Prunes (removes) all temporary environments.
    """
    prune_temp_environments()


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
