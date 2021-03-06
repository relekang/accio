import json
import os

from kombu import Exchange, Queue

from .logging import create_logger_config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)


def load_secrets():
    try:
        with open(os.path.join(REPO_DIR, 'secrets.json')) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


secrets = load_secrets()

RUNNING_TESTS = False
DEBUG = secrets.get('debug', True)
ALLOWED_HOSTS = secrets.get('allowed_hosts', [])
SECRET_KEY = secrets.get('secret_key', 'a secret')
WEBHOOK_SECRET_KEY = secrets.get('webhook_secret_key', 'super secret')

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'

SERVER_URL = secrets.get('server_url', 'http://127.0.0.1:8000')

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GITHUB_KEY = secrets.get('social_auth_github_key', '')
SOCIAL_AUTH_GITHUB_SECRET = secrets.get('social_auth_github_secret', '')

SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_GITHUB_SCOPE = ['read:org', 'repo', 'admin:repo_hook']

AUTHENTICATION_BACKENDS = (
    'social.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = [
    'accio.deployments',
    'accio.organizations',
    'accio.projects',
    'accio.users',

    'social.apps.django_app.default',
    'rest_framework',
    'djcelery',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

if secrets.get('raven_dsn', ''):
    import raven
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

    RAVEN_CONFIG = {
        'dsn': secrets.get('raven_dsn', ''),
        'release': raven.fetch_git_sha(REPO_DIR),
    }

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

RUN_TASKS_SYNCHRONOUSLY = DEBUG
BROKER_URL = 'redis://localhost:6379/4'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('extra', Exchange('extra')),
)

PRIVATE_KEY_FILENAME = secrets.get('private_key_filename', '~/.ssh/id_rsa')
PUBLIC_KEY_FILENAME = '{0}.pub'.format(secrets.get('private_key_filename', '~/.ssh/id_rsa'))

EMAIL_BACKEND = secrets.get('email_backend', 'django.core.mail.backends.console.EmailBackend')

LOGGING = create_logger_config(debug=DEBUG, **secrets.get('logging', {}))
