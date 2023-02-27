import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from garpix_utils.string import get_random_string
from django.utils.http import urlencode
import jwt


class KeycloakService:
    server_url = settings.KEYCLOAK.get('SERVER_URL')
    realm = settings.KEYCLOAK.get('REALM')
    client_id = settings.KEYCLOAK.get('CLIENT_ID')
    client_secret_key = settings.KEYCLOAK.get('CLIENT_SECRET_KEY')
    keyword = 'Bearer'

    def get_token(self, data):
        data = {
            "username": data['username'],
            "password": data['password'],
            "grant_type": 'password',
            "client_id": self.client_id
        }
        response = requests.post(
            f"{self.server_url}/auth/realms/{self.realm}/protocol/openid-connect/token",
            data=data,
            headers={"content-type": "application/x-www-form-urlencoded"}
        )

        if response.status_code != 200:
            return None

        return response.json().get('access_token', None)

    def get_token_by_code(self, code, request):

        data = {
            "code": code,
            "grant_type": 'authorization_code',
            "client_id": self.client_id,
            "client_secret": self.client_secret_key,
            "redirect_uri": request.build_absolute_uri(request.path)
        }
        response = requests.post(
            f"{self.server_url}/auth/realms/{self.realm}/protocol/openid-connect/token",
            data=data,
            headers={"content-type": "application/x-www-form-urlencoded"}
        )

        if response.status_code != 200:
            return None

        return response.json().get('access_token', None)

    def get_user(self, keycloak_user):

        User = get_user_model()

        user = User._default_manager.filter(keycloak_id=keycloak_user['sub']).first()

        if not user:
            user = User.create_keycloak_user(keycloak_user)

        return user

    def get_user_from_request(self, request):

        code = request.GET.get('code')

        token = self.get_token_by_code(code, request)

        if not token:
            return None

        keycloak_user = jwt.decode(token, options={"verify_signature": False})

        return self.get_user(keycloak_user)

    def get_keycloak_url(self, request, redirect_uri):
        state = get_random_string(64)
        nonce = get_random_string(64)

        request.session['keycloak_state'] = state
        request.session['keycloak_nonce'] = nonce

        redirect_uri = request.build_absolute_uri(redirect_uri)

        query_params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'state': state,
            'response_type': 'code',
            'scope': 'openid profile',
            'nonce': nonce
        }

        keycloak_url = f'{self.server_url}/auth/realms/{self.realm}/protocol/openid-connect/auth?{urlencode(query_params)}'

        return keycloak_url
