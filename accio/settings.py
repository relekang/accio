import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)


def load_secrets():
    try:
        with open(os.path.join(REPO_DIR, 'secrets.json')) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

secrets = load_secrets()

DEBUG = secrets.get('debug', True)
ALLOWED_HOSTS = secrets.get('allowed_hosts', [])
SECRET_KEY = secrets.get('secret_key', 'a secret')

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/admin/'

SOCIAL_AUTH_URL_NAMESPACE = 'social'


SOCIAL_AUTH_GITHUB_KEY = secrets.get('social_auth_github_key', '')
SOCIAL_AUTH_GITHUB_SECRET = secrets.get('social_auth_github_secret', '')

SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_GITHUB_SCOPE = ['read:org']

AUTHENTICATION_BACKENDS = (
    'social.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


INSTALLED_APPS = [
    'accio.organizations',
    'accio.projects',
    'accio.users',

    'social.apps.django_app.default',
    'rest_framework',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'PAGE_SIZE': 100,
}

ROOT_URLCONF = 'accio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'accio.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': secrets.get('db_name', 'accio'),
    }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(REPO_DIR, 'static')

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(REPO_DIR, 'uploads')
