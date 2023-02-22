from django.contrib.auth.models import AbstractUser
from garpix_notify.mixins import UserNotifyMixin

from garpix_keycloak.mixins import KeycloakUserMixin


class User(AbstractUser, UserNotifyMixin, KeycloakUserMixin):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
