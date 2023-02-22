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

Now when your request has `Bearer` token, it would be firstly checked as base django user token, then as keycloak token.

Enjoy!


# Changelog

See [CHANGELOG.md](CHANGELOG.md).

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)