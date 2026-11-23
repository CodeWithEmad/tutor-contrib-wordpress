FROM {{ WORDPRESS_OFFICIAL_IMAGE }}

# Install WooCommerce, the Open edX plugin and any extra plugins (curl ships with the base image).
# Plugins go to /usr/src/wordpress: the entrypoint copies them to /var/www/html on first start.
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends unzip; \
    for url in {{ WORDPRESS_WOOCOMMERCE_PLUGIN }} {{ WORDPRESS_OPENEDX_PLUGIN }}{% for plugin in WORDPRESS_EXTRA_PLUGINS %} {{ plugin }}{% endfor %}; do \
        curl -fsSL "$url" -o /tmp/plugin.zip; \
        unzip -oq /tmp/plugin.zip -d /usr/src/wordpress/wp-content/plugins/; \
        rm /tmp/plugin.zip; \
    done; \
    chown -R www-data:www-data /usr/src/wordpress/wp-content/plugins/; \
    apt-get purge -y --auto-remove unzip; \
    rm -rf /var/lib/apt/lists/*

# PHP limits (WooCommerce and media uploads often need more than the defaults)
RUN { \
        echo "memory_limit = {{ WORDPRESS_PHP_MEMORY_LIMIT }}"; \
        echo "upload_max_filesize = {{ WORDPRESS_UPLOAD_MAX_FILESIZE }}"; \
        echo "post_max_size = {{ WORDPRESS_UPLOAD_MAX_FILESIZE }}"; \
    } > /usr/local/etc/php/conf.d/tutor-wordpress.ini

EXPOSE 8080

# Listen on 8080 so Apache can run as a non-root user, and silence the ServerName warning
RUN set -eux; \
    echo "ServerName localhost" >> /etc/apache2/apache2.conf; \
    sed -i 's/^Listen 80$/Listen 8080/' /etc/apache2/ports.conf; \
    sed -i 's/<VirtualHost \*:80>/<VirtualHost *:8080>/' /etc/apache2/sites-available/000-default.conf; \
    grep -q "^Listen 8080$" /etc/apache2/ports.conf; \
    grep -q "<VirtualHost \*:8080>" /etc/apache2/sites-available/000-default.conf
