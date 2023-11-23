import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from garpix_utils.string import get_random_string
from django.utils.http import urlencode
import jwt

from garpix_keycloak.models import KeycloakGroup


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

    def get_token_by_code(self, code, request, redirect_uri):

        data = {
            "code": code,
            "grant_type": 'authorization_code',
            "client_id": self.client_id,
            "client_secret": self.client_secret_key,
            "redirect_uri": request.build_absolute_uri(redirect_uri)
        }
        response = requests.post(
            f"{self.server_url}/auth/realms/{self.realm}/protocol/openid-connect/token",
            data=data,
            headers={"content-type": "application/x-www-form-urlencoded"}
        )

        if response.status_code != 200:
            return None

        return response.json()

    def get_user(self, keycloak_user):

        User = get_user_model()

        user = User._default_manager.filter(keycloak_id=keycloak_user['sub']).first()

        try:
            if not user:
                user = User.create_keycloak_user(keycloak_user)

            prev_keycloak_groups = user.keycloak_groups.all().filter(group__isnull=False).values_list('group',
                                                                                                      flat=True)

            groups = list(user.groups.exclude(id__in=prev_keycloak_groups))

            keycloak_groups = []

            for _group in keycloak_user['realm_access']['roles']:
                keycloak_group, _ = KeycloakGroup.objects.get_or_create(name=_group)
                keycloak_groups.append(keycloak_group)
                if keycloak_group.group is not None:
                    groups.append(keycloak_group.group)

            user.keycloak_groups.set(keycloak_groups, clear=True)
            user.groups.set(groups, clear=True)

        except Exception as e:
            print(e)

        return user

    def get_user_from_request(self, request, code=None, redirect_url=None):

        code = code or request.GET.get('code')

        redirect_url = redirect_url or request.path

        token = self.get_token_by_code(code, request, redirect_url)

        if not token:
            return None

        token = token.get('access_token', None)

        keycloak_user = jwt.decode(token, options={"verify_signature": False})

        return self.get_user(keycloak_user)

    def get_user_data_by_token(self, token):

        keycloak_user = jwt.decode(token, options={"verify_signature": False})

        return keycloak_user

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

    def get_user_info_by_token(self, token):

        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "authorization": "Bearer " + token
        }
        response = requests.get(
            f"{self.server_url}/auth/realms/{self.realm}/protocol/openid-connect/userinfo",
            headers=headers
        )

        return response.json()
