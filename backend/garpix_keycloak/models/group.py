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

    def __str__(self):
        return str(self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        _prev_instance = self.__class__.objects.get(id=self.id) if self.id else None
        super(KeycloakGroup, self).save(force_insert, force_update, using, update_fields)
        if _prev_instance and self.group != _prev_instance.group:
            for _user in self.user_set.all():
                _user.groups.add(self.group)
                if _prev_instance.group is not None:
                    _user.groups.remove(_prev_instance.group)
