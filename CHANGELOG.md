
<a id='changelog-2.0.0'></a>
## v2.0.0 (2026-11-23)

- 💥[Improvement] Require Python 3.10+ (tested up to 3.14) and Tutor 20 to 22 (`tutor>=20,<23`). Older Tutor and Python versions stay on the 1.x release. (by @CodeWithEmad)
- [Feature] Add `WORDPRESS_RUN_LOCAL` to skip the WordPress container and only configure Open edX for an external WordPress site. (by @CodeWithEmad)
- [Feature] Add `WORDPRESS_DEBUG`, `WORDPRESS_CONFIG_EXTRA`, `WORDPRESS_PHP_MEMORY_LIMIT`, `WORDPRESS_UPLOAD_MAX_FILESIZE`, `WORDPRESS_EXTRA_PLUGINS` and `WORDPRESS_K8S_RESOURCES`. (by @CodeWithEmad)
- [Bugfix] `WORDPRESS_PORT` no longer breaks Caddy routing: the container always listens on 8080 and the Kubernetes service always exposes 8080. (by @CodeWithEmad)
- [Improvement] Update WordPress to 7.1.5, WooCommerce to 11.3.1 and the Open edX Commerce plugin to v2.1.1 (v2.1.2 ships no zip asset). (by @CodeWithEmad)
- [Improvement] Dockerfile: single plugin-install layer, precise Apache port edit, no wget. (by @CodeWithEmad)
- [Improvement] Publish to PyPI with trusted publishing; fix the Docker image workflow; test against Tutor 20, 21 and 22 in CI; move default branch to `main`. (by @CodeWithEmad)
- [Bugfix] `WORDPRESS_MYSQL_PORT` was never used; it is now part of `WORDPRESS_DB_HOST`. (by @CodeWithEmad)
- [Improvement] Remove the unused `wordpress-job` docker-compose service and Kubernetes job: the plugin has no init task for the wordpress service. (by @CodeWithEmad)
- [Improvement] Dockerfile: expose 8080 instead of the inherited 80. (by @CodeWithEmad)

<a id='changelog-1.2.0'></a>
## v1.2.0 (2025-04-16)

- [Improvement] Update WordPress official image version to 6.8.0-php8.1 (by @CodeWithEmad)

<a id='changelog-1.1.1'></a>
## v1.1.1 (2025-02-25)

- [Improvement] Migrate packaging from setup.py/setuptools to pyproject.toml/hatch. (by @CodeWithEmad)
- [Improvement] Support for tutor v19 added. (by @CodeWithEmad)

<a id='changelog-1.1.0'></a>
## v1.1.0 (2024-11-27)

- [Feature] Added comprehensive WordPress integration for Open edX including:
  - Full WordPress installation and configuration management
  - Integration with Open edX Commerce WordPress Plugin and WooCommerce
  - Configurable WordPress settings including version, host, ports, and database options
  (by @CodeWithEmad)

<a id='changelog-1.0.1'></a>
## v1.0.1 (2024-07-27)

- [Improvement] Support for Python < 3.9 (by @CodeWithEmad)

<a id='changelog-1.0.0'></a>
## v1.0.0 (2024-07-25)

- [Improvement] Plugin Burn - First Release! 🔥(by @CodeWithEmad)
