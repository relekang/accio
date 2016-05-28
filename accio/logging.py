import os


def create_logger_config(path=None, django_level='INFO', accio_level='DEBUG', debug=False):
    handlers = ['file', 'sentry']
    if path is None:
        path = os.environ.get('ACCIO_LOG_PATH', 'accio.log')

    if debug:
        handlers = ['console']

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
            'raven': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'WARNING',
                'class': 'raven.contrib.django.handlers.SentryHandler',
                'formatter': 'raven'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': path,
                'formatter': 'verbose'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django': {
                'handlers': handlers,
                'propagate': True,
                'level': django_level,
            },
            'accio': {
                'handlers': handlers,
                'level': accio_level,
            },
        }
    }
