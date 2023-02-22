from garpixcms.settings import *  # noqa

MIGRATION_MODULES.update({  # noqa:F405
    'fcm_django': 'app.migrations.fcm_django'
})

INSTALLED_APPS += [
    'garpix_keycloak'
]

KEYCLOAK = {
    'SERVER_URL': 'https://keycloak-test.infra.garpix.com/auth',
    'REALM': 'django-test',
    'CLIENT_ID': 'client-backend',
    'CLIENT_SECRET_KEY': 'ixtg3YCIeBTEKiPMeJVVOV11qarGBTfH'
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
