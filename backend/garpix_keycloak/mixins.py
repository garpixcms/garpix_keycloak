from django.db import models
from django.utils.translation import gettext_lazy as _
from garpix_utils.string import get_random_string


class KeycloakUserMixin(models.Model):
    keycloak_id = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Keycloak ID'))

    class Meta:
        abstract = True

    @classmethod
    def create_keycloak_user(cls, keycloak_data):
        cls.objects.create_user(keycloak_id=keycloak_data['sub'], first_name=keycloak_data['given_name'],
                                last_name=keycloak_data['given_name'], username=keycloak_data['username'],
                                password=get_random_string(25), email=keycloak_data['email'])
