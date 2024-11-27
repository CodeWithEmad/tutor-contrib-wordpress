# Use the official WordPress image
FROM {{ WORDPRESS_OFFICIAL_IMAGE }}

# Install necessary utilities
RUN apt-get update && \
    apt-get install -y wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Download and install WooCommerce
RUN wget {{ WORDPRESS_WOOCOMMERCE_PLUGIN }} -O /tmp/woocommerce.zip && \
    unzip -o /tmp/woocommerce.zip -d /usr/src/wordpress/wp-content/plugins/ && \
    rm /tmp/woocommerce.zip

# Download and install the OpenEdX WordPress plugin
RUN wget {{ WORDPRESS_OPENEDX_PLUGIN }} -O /tmp/openedx-commerce.zip && \
    unzip -o /tmp/openedx-commerce.zip -d /usr/src/wordpress/wp-content/plugins/ && \
    rm /tmp/openedx-commerce.zip

# Set proper permissions
RUN chown -R www-data:www-data /usr/src/wordpress/wp-content/plugins/

# Clean up
RUN apt-get purge -y wget unzip && \
    apt-get autoremove -y

# Add ServerName directive to suppress Apache warning
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Configure Apache to listen on port 8080
RUN sed -i 's/80/8080/g' /etc/apache2/ports.conf /etc/apache2/sites-available/000-default.conf
