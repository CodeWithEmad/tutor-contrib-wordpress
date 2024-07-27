WordPress Plugin for `Tutor`_
#############################

.. image:: https://img.shields.io/pypi/v/tutor-contrib-wordpress?logo=python&logoColor=white
   :alt: PyPI releases
   :target: https://pypi.org/project/tutor-contrib-wordpress

.. image:: https://img.shields.io/github/license/codewithemad/tutor-contrib-wordpress.svg?style=flat-square
   :alt: AGPL License
   :target: https://www.gnu.org/licenses/agpl-3.0.en.html

Overview
--------

This is a `Tutor`_ plugin for integrating the `Open edX Commerce WordPress Plugin`_ with your Open edX instance.
The plugin allows seamless synchronization and interaction between your WordPress site and Open edX platform,
providing a cohesive e-commerce experience. If you don't know how to install the WordPress plugin, check out
this `installation guide`_.

Prerequisites
-------------

- A running WordPress site with the `Open edX Commerce WordPress Plugin`_ installed.
- Installation of Tutor version >= 15.0.0.

Installation
------------

Ensure you are using Tutor v15+ (Olive onwards). First, install the plugin by running:

.. code-block:: bash

    pip install -U tutor-contrib-wordpress

Enable the plugin and run the launch command:

.. code-block:: bash

    tutor plugins enable wordpress
    tutor dev|local|k8s launch

Alternatively, if you already have a running Open edX instance, just run the necessary jobs:

.. code-block:: bash

    tutor dev|local|k8s do init --limit=wordpress

Configuration
-------------

Inside your WordPress admin panel, you will need to configure the following values:

- **Open edX Domain**
- **Client ID**
- **Client Secret**

.. image:: https://raw.githubusercontent.com/codewithemad/tutor-contrib-wordpress/master/images/openedx-sync-plugin-settings.png
   :alt: Open edX Sync Plugin Settings in your WordPress Settings


You can retrieve these configuration values by running:

.. code-block:: bash

    tutor wordpress config


.. code-block:: text

    ===============================================
            WordPress Plugin Configurations
    ===============================================

    Open edX Domain: http://local.edly.io
    Client ID: qjCayDktffXrU09N17NrslKyWQ2EwzWn
    Client ID (dev): JDx6Uy0hN67VUfacxKcLyYQz7HK9liVx
    Client Secret: P4w82huaZQdyz4qolknsIHYneGEoIggc


Or by using Tutor to print them individually:

.. code-block:: bash

    tutor config printvalue LMS_HOST
    tutor config printvalue WORDPRESS_OAUTH2_SECRET
    tutor config printvalue WORDPRESS_OAUTH2_KEY_SSO
    tutor config printvalue WORDPRESS_OAUTH2_KEY_SSO_DEV

Contributing
------------

We welcome all contributions! Feel free to open a Pull Request.

License
-------

This software is licensed under the terms of the `AGPLv3`_.

.. _Tutor: https://docs.tutor.edly.io
.. _installation guide: https://docs.openedx.org/projects/wordpress-ecommerce-plugin/en/latest/plugin_quickstart.html
.. _Open edX Commerce WordPress Plugin: https://github.com/openedx/openedx-wordpress-ecommerce
.. _AGPLv3: https://github.com/codewithemad/tutor-contrib-wordpress/blob/master/LICENSE.txt
