from __future__ import annotations

from glob import glob
import os
import sys
import typing as t

import click
from tutor import fmt, hooks as tutor_hooks, config as tutor_config
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

# Support for older Python versions
if sys.version_info >= (3, 9):
    import importlib_resources
else:
    import pkg_resources

# Handle version suffix in nightly mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

###############
# CONFIGURATION
###############

tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        ("WORDPRESS_VERSION", __version__),
        ("WORDPRESS_HOST", "site.{{ LMS_HOST }}"),
        ("WORDPRESS_PORT", "8080"),
        # https://hub.docker.com/_/wordpress/
        ("WORDPRESS_OFFICIAL_IMAGE", "wordpress:6.7.1-php8.1"),
        (
            "WORDPRESS_DOCKER_IMAGE",
            "docker.io/codewithemad/tutor-wordpress:{{ WORDPRESS_VERSION }}",
        ),
        ("WORDPRESS_MYSQL_HOST", "{{ MYSQL_HOST }}"),
        ("WORDPRESS_MYSQL_PORT", "{{ MYSQL_PORT }}"),
        ("WORDPRESS_MYSQL_DATABASE", "wordpress"),
        ("WORDPRESS_MYSQL_USERNAME", "wordpress"),
        ("WORDPRESS_TABLE_PREFIX", "wp_"),
        ("WORDPRESS_DATA_VOLUME_SIZE", "5Gi"),
        (
            "WORDPRESS_OPENEDX_PLUGIN",
            "https://github.com/openedx/openedx-wordpress-ecommerce/releases/download/v2.0.7/openedx-commerce.zip",
        ),
        (
            "WORDPRESS_WOOCOMMERCE_PLUGIN",
            "https://downloads.wordpress.org/plugin/woocommerce.9.4.2.zip",
        ),
    ]
)

tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'WORDPRESS_'.
        ("WORDPRESS_OAUTH2_SECRET", "{{ 32|random_string }}"),
        ("WORDPRESS_OAUTH2_KEY_SSO", "{{ 32|random_string }}"),
        ("WORDPRESS_OAUTH2_KEY_SSO_DEV", "{{ 32|random_string }}"),
        ("WORDPRESS_MYSQL_PASSWORD", "{{ 32|random_string }}"),
    ]
)

######################
# INITIALIZATION TASKS
######################

MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    ("lms", ("wordpress", "tasks", "lms", "init.sh")),
    ("mysql", ("wordpress", "tasks", "mysql", "init.sh")),
]


def get_template_full_path(package_name: str, *template_path: str) -> str:
    if sys.version_info >= (3, 9):
        return str(
            importlib_resources.files(package_name)
            / os.path.join("templates", *template_path)
        )
    else:
        resource_path = pkg_resources.resource_filename(package_name, "")
        return os.path.join(resource_path, "templates", *template_path)


for service, template_path in MY_INIT_TASKS:
    full_path: str = get_template_full_path("tutorwordpress", *template_path)
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


#########################
# DOCKER IMAGE MANAGEMENT
#########################

tutor_hooks.Filters.IMAGES_BUILD.add_item(
    (
        "wordpress",
        ("plugins", "wordpress", "build", "wordpress"),
        "{{ WORDPRESS_DOCKER_IMAGE }}",
        (),
    )
)
tutor_hooks.Filters.IMAGES_PULL.add_items(
    [
        (
            "wordpress",
            "{{ WORDPRESS_DOCKER_IMAGE }}",
        ),
    ]
)
tutor_hooks.Filters.IMAGES_PUSH.add_item(
    (
        "wordpress",
        "{{ WORDPRESS_DOCKER_IMAGE }}",
    )
)

####################
# TEMPLATE RENDERING
####################

tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        str(get_template_full_path("tutorwordpress", "")),
    ]
)

tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutorwordpress/templates/wordpress/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/wordpress/build``.
    [
        ("wordpress/build", "plugins"),
        ("wordpress/apps", "plugins"),
    ],
)


################
# PATCH LOADING
################

# For each file in tutorwordpress/patches,
# apply a patch based on the file's name and contents.
if sys.version_info >= (3, 9):
    glob_pattern = str(importlib_resources.files("tutorwordpress") / "patches" / "*")
else:
    glob_pattern = os.path.join(
        pkg_resources.resource_filename("tutorwordpress", "patches"), "*"
    )

for path in glob(glob_pattern):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )

#####################
# CUSTOM CLI COMMANDS
#####################


@click.group()
def wordpress() -> None:
    pass


tutor_hooks.Filters.CLI_COMMANDS.add_item(wordpress)


@wordpress.command()
@click.pass_context
def config(context: click.Context) -> None:
    """
    Print out the configurations used in WordPress plugin.
    """
    config = tutor_config.load(context.obj.root)
    https_enabled = config["ENABLE_HTTPS"]
    protocol = "https" if https_enabled else "http"
    lms_host = f"{protocol}://{config['LMS_HOST']}"
    wordpress_host = f"{protocol}://{config['WORDPRESS_HOST']}"
    if not https_enabled:
        lms_host += ":8000"
        wordpress_host += f":{config['WORDPRESS_PORT']}"

    click.echo(fmt.title("WordPress Plugin Configurations"))
    info_text = (
        "\n"
        f"Client ID: {config['WORDPRESS_OAUTH2_KEY_SSO']} \n"
        f"Client ID (dev): {config['WORDPRESS_OAUTH2_KEY_SSO_DEV']} \n"
        f"Client Secret: {config['WORDPRESS_OAUTH2_SECRET']} \n"
        "\n"
        f"Open edX Domain: {lms_host} \n"
        f"Wordpress Domain: {wordpress_host}"
    )
    fmt.echo_info(info_text)
