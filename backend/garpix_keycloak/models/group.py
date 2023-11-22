from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Manager
from django.utils.translation import gettext_lazy as _


class KeycloakGroup(models.Model):
    name = models.CharField(_('name'), max_length=150, unique=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    objects = Manager()

    class Meta:
        verbose_name = _('Keycloak group')
        verbose_name_plural = _('Keycloak groups')
