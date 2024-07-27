from __future__ import annotations

import os
import sys

import click
from tutor import fmt, hooks, config as tutor_config

from .__about__ import __version__

if sys.version_info >= (3, 9):
    from importlib.resources import files as importlib_resources_files
else:
    import pkg_resources

###############
# CONFIGURATION
###############

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'WORDPRESS_'.
        ("WORDPRESS_VERSION", __version__),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'WORDPRESS_'.
        ("WORDPRESS_OAUTH2_SECRET", "{{ 32|random_string }}"),
        ("WORDPRESS_OAUTH2_KEY_SSO", "{{ 32|random_string }}"),
        ("WORDPRESS_OAUTH2_KEY_SSO_DEV", "{{ 32|random_string }}"),
    ]
)

######################
# INITIALIZATION TASKS
######################

MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    ("lms", ("wordpress", "tasks", "lms", "init.sh")),
]


def get_template_full_path(package_name: str, *template_path: str) -> str:
    if sys.version_info >= (3, 9):
        return str(
            importlib_resources_files(package_name)
            / os.path.join("templates", *template_path)
        )
    else:
        resource_path = pkg_resources.resource_filename(package_name, "")
        return os.path.join(resource_path, "templates", *template_path)


for service, template_path in MY_INIT_TASKS:
    full_path: str = get_template_full_path("tutorwordpress", *template_path)
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))

#####################
# CUSTOM CLI COMMANDS
#####################


@click.group()
def wordpress() -> None:
    pass


hooks.Filters.CLI_COMMANDS.add_item(wordpress)


@wordpress.command()
@click.pass_context
def config(context: click.Context) -> None:
    """
    Print out the configurations used in WordPress plugin.
    """
    config = tutor_config.load(context.obj.root)
    protocol = "https" if config["ENABLE_HTTPS"] else "http"
    lms_host = f"{protocol}://{config['LMS_HOST']}"
    click.echo(fmt.title("WordPress Plugin Configurations"))
    fmt.echo_info(
        "\n"
        f"Open edX Domain: {lms_host} \n"
        f"Client ID: {config['WORDPRESS_OAUTH2_KEY_SSO']} \n"
        f"Client ID (dev): {config['WORDPRESS_OAUTH2_KEY_SSO_DEV']} \n"
        f"Client Secret: {config['WORDPRESS_OAUTH2_SECRET']} \n"
    )
