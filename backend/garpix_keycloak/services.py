import requests
from django.conf import settings
from django.contrib.auth import get_user_model


class KeycloakService:
    server_url = settings.KEYCLOAK.get('SERVER_URL')
    realm = settings.KEYCLOAK.get('REALM')
    client_id = settings.KEYCLOAK.get('CLIENT_ID')
    client_secret_key = settings.KEYCLOAK.get('CLIENT_SECRET_KEY')
    keyword = 'Bearer'
    keycloak_user = None

    def get_token(self, data):
        data = {
            "username": data['username'],
            "password": data['password'],
            "grant_type": 'password',
            "client_id": 'admin-cli',
        }
        response = requests.post(
            f"{self.server_url}/realms/{self.realm}/protocol/openid-connect/token",
            data=data,
            headers={"content-type": "application/x-www-form-urlencoded"}
        )

        if response.status_code != 200:
            return None

        return response.json().get('access_token', None)

    def get_user(self, request):

        if 'HTTP_AUTHORIZATION' not in request.META:
            return None

        token = request.META['HTTP_AUTHORIZATION']
        token = token[len(self.keyword) + 1:]

        data = {
            "token": token,
            "client_id": self.client_id,
            "client_secret": self.client_secret_key,
        }
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "authorization": f"{self.keyword} {token}",
        }
        response = requests.post(
            f"{self.server_url}/realms/{self.realm}/protocol/openid-connect/token/introspect",
            data=data,
            headers=headers
        )

        if response.status_code != 200 or not response.json()['active']:
            return None

        self.keycloak_user = response.json()

        User = get_user_model()

        user = User._default_manager.filter(keycloak_id=self.keycloak_user['sub']).first()

        if not user:
            user = User.create_keycloak_user(self.keycloak_user)

        return user
