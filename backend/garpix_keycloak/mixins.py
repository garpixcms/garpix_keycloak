from django.db import models
from django.utils.translation import gettext_lazy as _
from garpix_utils.string import get_random_string
from django.db.models import Q

from garpix_keycloak.models import KeycloakGroup


class KeycloakUserMixin(models.Model):
    keycloak_id = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Keycloak ID'))

    keycloak_groups = models.ManyToManyField(
        KeycloakGroup,
        verbose_name=_('keycloak groups'),
        blank=True,
        help_text=_(
            'The keycloak groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    @classmethod
    def create_keycloak_user(cls, keycloak_data):
        user = cls.objects.filter(
            Q(email=keycloak_data['email'], username=keycloak_data['preferred_username']) | Q(email__isnull=True,
                                                                                              username=keycloak_data[
                                                                                                  'preferred_username'])).first()

        if user:
            user.keycloak_id = keycloak_data['sub']
            user.save()
        else:
            user = cls.objects.create_user(keycloak_id=keycloak_data['sub'], first_name=keycloak_data['given_name'],
                                           last_name=keycloak_data['family_name'],
                                           username=keycloak_data['preferred_username'],
                                           password=get_random_string(25), email=keycloak_data['email'])

        return user
