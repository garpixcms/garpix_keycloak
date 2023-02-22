from django.contrib.auth.middleware import AuthenticationMiddleware

from garpix_keycloak.services import KeycloakService


class KeycloakAuthMiddleware(AuthenticationMiddleware):
    def process_request(self, request):

        if not request.user.is_authenticated:
            user = KeycloakService().get_user(request)

            if user:
                request.user = user
