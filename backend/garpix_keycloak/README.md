# Garpix Keycloak

Keycloak uth module for Django/DRF projects. Part of GarpixCMS.

Used packages: 

* [django rest framework](https://www.django-rest-framework.org/api-guide/authentication/)
* etc; see setup.py

## Quickstart

Install with pip:

```bash
pip install garpix_keycloak
```

Add the `garpix_keycloak` to your `INSTALLED_APPS`:

```python
# settings.py

# ...
INSTALLED_APPS = [
    # ...
    'garpix_keycloak',
]
```

Add `KeycloakUserMixin` to your `User` model:

```python
from django.contrib.auth.models import AbstractUser

from garpix_keycloak.mixins import KeycloakUserMixin


class User(AbstractUser, KeycloakUserMixin):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

```

Add `KeycloakAuthMiddleware` to `MIDDLEWARE` settings after `django.contrib.auth.middleware.AuthenticationMiddleware`:

```python
# settings.py


MIDDLEWARE = [
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'garpix_keycloak.middlewares.KeycloakAuthMiddleware',
]
```

Add authentication backend:

```python
AUTHENTICATION_BACKENDS = [
    # ...
    'garpix_keycloak.backends.KeycloakAuthenticationBackend'
]
```

Add keycloak parameters to `settings.py`:

```python
# settings.py


KEYCLOAK = {
    'SERVER_URL': 'your_server_url',
    'REALM': 'your_realm',
    'CLIENT_ID': 'your_client_id',
    'CLIENT_SECRET_KEY': 'your_client_secret_key'
}

```

Use `get_keycloak_url` from `KeycloakService` to generate keycloak log in link.

`garpix_keycloak` creates `User` model instance, using `create_keycloak_user` class method. 
You can override it if you need some customization in your project.

Enjoy!


# Changelog

See [CHANGELOG.md](CHANGELOG.md).

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)