# Modify users created an incorrect email and that might clash with the newly created users
./manage.py lms shell -c \
  "from django.contrib.auth import get_user_model;\
  get_user_model().objects.filter(username='wordpress').exclude(email='wordpress@openedx').update(email='wordpress@openedx')"

# Create an oauth2 application for wordpress woocommerce
# https://docs.openedx.org/projects/wordpress-ecommerce-plugin/en/latest/how-tos/create_an_openedx_app.html
# wordpress user must be staff a staff to create, edit, and delete enrollments.
./manage.py lms manage_user wordpress wordpress@openedx --staff  --unusable-password
./manage.py lms create_dot_application \
  --grant-type authorization-code \
  --client-id {{ WORDPRESS_OAUTH2_KEY_SSO }} \
  --client-secret {{ WORDPRESS_OAUTH2_SECRET }} \
  --scopes user_id \
  --skip-authorization \
  --update wordpress-sso wordpress
./manage.py lms create_dot_application \
  --grant-type authorization-code \
  --client-id {{ WORDPRESS_OAUTH2_KEY_SSO_DEV }} \
  --client-secret {{ WORDPRESS_OAUTH2_SECRET }} \
  --scopes user_id \
  --skip-authorization \
  --update wordpress-sso-dev wordpress