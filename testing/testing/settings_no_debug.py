from testing.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

try:
    import transmeta
    TRANSMETA_DEFAULT_LANGUAGE = 'en'
    INSTALLED_APPS += ('transmeta',
                        'testing.inplace_transmeta')
    MIDDLEWARE_CLASSES += (
        'django.middleware.locale.LocaleMiddleware',
        'testing.inplace_transmeta.middleware.LocaleMiddleware')
except ImportError:
    pass
