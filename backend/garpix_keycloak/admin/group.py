from django.contrib import admin

from garpix_keycloak.models import KeycloakGroup


@admin.register(KeycloakGroup)
class KeycloakGroupAdmin(admin.ModelAdmin):
    pass
