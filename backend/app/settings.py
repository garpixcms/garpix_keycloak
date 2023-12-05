from garpixcms.settings import *  # noqa

MIGRATION_MODULES.update({  # noqa:F405
    'fcm_django': 'app.migrations.fcm_django'
})

INSTALLED_APPS += [
    'garpix_keycloak'
]

KEYCLOAK = {
    'SERVER_URL': 'your_server_url',
    'REALM': 'your_realm',
    'CLIENT_ID': 'your_client_id',
    'CLIENT_SECRET_KEY': 'your_client_secret_key'
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'garpix_keycloak.middlewares.KeycloakAuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'garpixcms.middleware.locale.GarpixLocaleMiddleware'
]

AUTHENTICATION_BACKENDS += [
    'garpix_keycloak.backends.KeycloakAuthenticationBackend'
]

ISO_LOGS_NAME = 'garpix_keycloak'
IB_ISO_LOGS_NAME = 'garpix_keycloak_ib'
SYSTEM_ISO_LOGS_NAME = 'garpix_keycloak_system'
