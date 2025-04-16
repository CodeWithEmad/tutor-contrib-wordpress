WordPress Plugin for `Tutor`_
#############################

.. image:: https://img.shields.io/pypi/v/tutor-contrib-wordpress?logo=python&logoColor=white
   :alt: PyPI releases
   :target: https://pypi.org/project/tutor-contrib-wordpress

.. image:: https://static.pepy.tech/badge/tutor-contrib-wordpress
   :alt: PyPI Downloads
   :target: https://pepy.tech/projects/tutor-contrib-wordpress

.. image:: https://img.shields.io/github/license/codewithemad/tutor-contrib-wordpress.svg?style=flat-square
   :alt: AGPL License
   :target: https://www.gnu.org/licenses/agpl-3.0.en.html

Overview
********

This is a `Tutor`_ plugin that provides complete WordPress integration with your Open edX instance. It includes:

- Full WordPress installation and management
- Integration with the `Open edX Commerce WordPress Plugin`_

If you need help installing the WordPress plugin, check out this `installation guide`_.

Prerequisites
*************

- Installation of Tutor version >= 15.0.0
- MySQL database (can use the same one as Open edX)

Installation
************

Ensure you are using Tutor v15+ (Olive onwards). First, install the plugin by running:

.. code-block:: bash

    pip install -U tutor-contrib-wordpress
    # or with tutor
    tutor plugins install wordpress

Enable the plugin and run the launch command:

.. code-block:: bash

    tutor plugins enable wordpress
    tutor dev|local|k8s launch

Alternatively, if you already have a running Open edX instance, just run the necessary jobs:

.. code-block:: bash

    tutor dev|local|k8s do init --limit=wordpress
    tutor dev|local|k8s start wordpress

Configuration
*************

The plugin automatically installs WordPress with the Open edX Commerce and Woocommerce plugins. Inside your WordPress
admin panel, go to Settings -> Open edX Sync plugin, and configure:

- **Open edX Domain**
- **Client ID**
- **Client Secret**

To verify the connection, click on "Generate JWT Token". If the process is successful, a new token will be generated.

.. image:: https://raw.githubusercontent.com/codewithemad/tutor-contrib-wordpress/master/images/openedx-sync-plugin-settings.png
   :alt: Open edX Sync Plugin Settings in your WordPress Settings

You can retrieve these configuration values by running:

.. code-block:: bash

    tutor dev|local|k8s do wordpress config

This command will output the current configurations, including the Client ID, Client Secret, Open edX Domain,
and WordPress Domain. Here is an example of the output:

.. code-block:: text

    ===============================================
        WordPress Plugin Configurations
    ===============================================

    Client ID: vvpTamiepPwjZhr0uOQGr5PhYBzp2hQw 
    Client ID (dev): MlbXk1V3wB7nWPAAyLF3McyfBBMqExa4 
    Client Secret: MdrgbtU8Q94He3gejF6Zf5MDookoeozO 

    Open edX Domain: http://local.edly.io:8000 
    Wordpress Domain: http://site.local.edly.io:8080

Variables
*********

The plugin supports the following configuration variables:

- ``WORDPRESS_VERSION``: Plugin version
- ``WORDPRESS_HOST``: WordPress site hostname
- ``WORDPRESS_PORT``: WordPress port (default: 8080)
- ``WORDPRESS_DOCKER_IMAGE``: Docker image for WordPress
- ``WORDPRESS_OPENEDX_PLUGIN``: URL to the Open edX Commerce plugin
- ``WORDPRESS_WOOCOMMERCE_PLUGIN``: (default: "https://downloads.wordpress.org/plugin/woocommerce.9.4.2.zip")
  The WooCommerce plugin zip file URL. You can specify a different version if needed.
- ``WORDPRESS_OFFICIAL_IMAGE``: (default: "wordpress:6.8.0-php8.1")
  The official WordPress Docker image used as the base for building the plugin's custom image.
  This image includes PHP and Apache server. You can specify a different version or PHP variant if needed.

Database Settings
=================

- ``WORDPRESS_MYSQL_HOST``: MySQL host
- ``WORDPRESS_MYSQL_PORT``: MySQL port
- ``WORDPRESS_MYSQL_DATABASE``: Database name (default: wordpress)
- ``WORDPRESS_MYSQL_USERNAME``: Database username
- ``WORDPRESS_MYSQL_PASSWORD``: Database password (auto-generated)
- ``WORDPRESS_TABLE_PREFIX``: Table prefix (default: ``wp_``)

Storage Settings
================

- ``WORDPRESS_DATA_VOLUME_SIZE``: Size of WordPress persistent volume (default: 5Gi)

OAuth2 Settings
===============

- ``WORDPRESS_OAUTH2_SECRET``: OAuth2 secret key (auto-generated)
- ``WORDPRESS_OAUTH2_KEY_SSO``: OAuth2 client ID (auto-generated)
- ``WORDPRESS_OAUTH2_KEY_SSO_DEV``: OAuth2 development client ID (auto-generated)

Contributing
************

We welcome all contributions! Feel free to open a Pull Request or an Issue.

License
*******

This software is licensed under the terms of the `AGPLv3`_.

.. _Tutor: https://docs.tutor.edly.io
.. _Open edX Commerce WordPress Plugin: https://github.com/openedx/openedx-wordpress-ecommerce
.. _AGPLv3: https://github.com/codewithemad/tutor-contrib-wordpress/blob/master/LICENSE.txt
.. _installation guide: https://docs.openedx.org/projects/wordpress-ecommerce-plugin/en/latest/plugin_quickstart.html
