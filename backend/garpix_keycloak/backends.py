from garpix_keycloak.services import KeycloakService


class KeycloakAuthenticationBackend:
    def authenticate(self, request):
        try:
            return KeycloakService().get_user_from_request(request)
        except Exception:
            return None
