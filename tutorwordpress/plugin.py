from __future__ import annotations

from importlib.resources import files

import click
from tutor import fmt, hooks as tutor_hooks, config as tutor_config
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

ROOT = files("tutorwordpress")

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
        # Run WordPress in Tutor. Set to false to only configure Open edX for an external site.
        ("WORDPRESS_RUN_LOCAL", True),
        # Host port published in dev mode. The container always listens on 8080.
        ("WORDPRESS_PORT", "8080"),
        # Dev mode only: enable WP_DEBUG and debug logging
        ("WORDPRESS_DEBUG", True),
        # PHP code appended to wp-config.php on first start (e.g. define('WP_HOME', ...);).
        # The official image already trusts X-Forwarded-Proto, so HTTPS behind Caddy works.
        ("WORDPRESS_CONFIG_EXTRA", ""),
        ("WORDPRESS_PHP_MEMORY_LIMIT", "256M"),
        ("WORDPRESS_UPLOAD_MAX_FILESIZE", "64M"),
        # Kubernetes resource requests/limits for the wordpress container
        ("WORDPRESS_K8S_RESOURCES", {}),
        # https://hub.docker.com/_/wordpress/
        ("WORDPRESS_OFFICIAL_IMAGE", "wordpress:7.1.5-php8.4"),
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
            "https://github.com/openedx/openedx-wordpress-ecommerce/releases/download/v2.1.1/openedx-commerce.zip",
        ),
        (
            "WORDPRESS_WOOCOMMERCE_PLUGIN",
            "https://downloads.wordpress.org/plugin/woocommerce.11.3.1.zip",
        ),
        # URLs of additional plugin zip files to install in the image
        ("WORDPRESS_EXTRA_PLUGINS", []),
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


for service, template_path in MY_INIT_TASKS:
    init_task: str = (
        (ROOT / "templates").joinpath(*template_path).read_text(encoding="utf-8")
    )
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
        str(ROOT / "templates"),
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
    ],
)


################
# PATCH LOADING
################

# For each file in tutorwordpress/patches,
# apply a patch based on the file's name and contents.
for path in (ROOT / "patches").iterdir():
    tutor_hooks.Filters.ENV_PATCHES.add_item(
        (path.name, path.read_text(encoding="utf-8"))
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
        if config["WORDPRESS_RUN_LOCAL"]:
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
