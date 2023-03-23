from django.contrib.auth import get_user_model

from garpix_keycloak.services import KeycloakService


class KeycloakAuthenticationBackend:
    def authenticate(self, request):
        try:
            return KeycloakService().get_user_from_request(request)
        except Exception:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().active_objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
