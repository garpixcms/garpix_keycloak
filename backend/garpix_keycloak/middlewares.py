from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth import login
from garpix_keycloak.services import KeycloakService


class KeycloakAuthMiddleware(AuthenticationMiddleware):
    def process_request(self, request):

        request_data = request.GET

        if not request.user.is_authenticated and 'keycloak_state' in request.session and 'state' in request_data and 'code' in request_data and request_data.get(
                'state') == request.session['keycloak_state']:

            user = KeycloakService().get_user_from_request(request)

            if user:
                login(request, user)
