
from garpix_keycloak.services import KeycloakService
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
from django.contrib.auth.models import AnonymousUser


def get_user_by_kk_token(token):

    try:
        token_data = KeycloakService().get_user_data_by_token(token)

        if settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS > 0:
            if token_data['expires_in'] < settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS:
                raise Exception("Token expired.")
        return KeycloakService().get_user(token_data)
    except Exception as e:
        print(str(e))

    return AnonymousUser()


def get_token_from_request(request, keyword='Bearer'):
    header_key = settings.GARPIX_USER.get('KEYCLOAK_REST_AUTH_HEADER_KEY', 'HTTP_X_AUTHORIZATION')
    if header_key not in request.META:
        return None

    token = request.META[header_key]
    token = token[len(keyword) + 1:]
    return token


class KeycloakAuthentication(TokenAuthentication):

    keyword = 'Bearer'

    def authenticate(self, request):

        token = get_token_from_request(request, keyword=self.keyword)

        if token is None:
            return None

        user = get_user_by_kk_token(token)

        if user is not None:
            return user, None
        return user, None
