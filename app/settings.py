import os

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    YANDEX_MONEY_DEBUG=(bool, False),
    EMAIL_USE_TLS=(bool, True),
)
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

GOOGLE_RECAPTCHA_SECRET_KEY = env('GOOGLE_RECAPTCHA_SECRET_KEY')

YANDEX_MONEY_DEBUG = env('YANDEX_MONEY_DEBUG')
YANDEX_MONEY_SCID = env('YANDEX_MONEY_SCID')
YANDEX_MONEY_SHOP_ID = env('YANDEX_MONEY_SHOP_ID')
YANDEX_MONEY_SHOP_PASSWORD = env('YANDEX_MONEY_SHOP_PASSWORD')
YANDEX_MONEY_FAIL_URL = 'https://avtopilot1.ru/fail-payment/'
YANDEX_MONEY_SUCCESS_URL = 'https://avtopilot1.ru/success-payment/'
# информировать о случаях, когда модуль вернул Яндекс.Кассе ошибку
YANDEX_MONEY_MAIL_ADMINS_ON_PAYMENT_ERROR = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

RECIPIENT_LIST = env.list('RECIPIENT_LIST')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Application definition

INSTALLED_APPS = [
    'easy_thumbnails',
    'filer',
    'mptt',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'robots',
    'django_cleanup',
    'app',
    'adminsortable2',
    'adminsortable',
    'django_ace',
    'ckeditor',
    'ckeditor_uploader',
    'webpack_loader',
    'sitetree',
    'navigation',
    'catalog',
    'comment',
    'accounts',
    'order',
    'page',
    'settings',
    'slider',
    'vacations',
    'promotion',
    'search',
    'yandex_money',
    'builder',
    'lp.apps.LpConfig',
]

SITE_ID = 1

HTML_MINIFY = not DEBUG

SITE_URL = 'https://avtopilot-moskow.ru/'

AUTH_USER_MODEL = 'accounts.User'  # changes the built-in user model to ours
LOGIN_REDIRECT_URL = 'account'
LOGOUT_REDIRECT_URL = 'login'

X_FRAME_OPTIONS = 'ALLOW'

THUMBNAIL_HIGH_RESOLUTION = True

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    # 'htmlmin.middleware.MarkRequestMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'comment/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.cart_info',
                'app.context_processors.options',
                'app.context_processors.makes_404',
                'app.context_processors.menu',
                'app.context_processors.forms',
                'catalog.context_processors.widget_catalog',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app/static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'dist')
# ]

CKEDITOR_UPLOAD_PATH = ''
CKEDITOR_RESTRICT_BY_DATE = False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Custom': [
            {'name': 'document', 'items': ['Source', 'Preview']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Replace', '-', 'SelectAll']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'insert',
             'items': ['Image', 'Table', 'HorizontalRule', 'SpecialChar']},
            '/',
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'styles', 'items': ['Styles', 'Format', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
        ],
        'toolbar': 'Custom',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': 400,
        'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embed',
            'embedbase',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            # 'dialog',
            # 'dialogui',
            'elementspath',
            # 'youtube',
        ]),
    },
    'special': {
        # 'skin': 'icy_orange',
        'toolbar': 'Special',
        'removePlugins': 'elementspath',
        'width': '100%',
        'toolbar_Special': [
            ['Bold', 'Italic', 'Underline']
        ]
    }
}

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Автопилот Москва',

    # menu
    'SEARCH_URL': '',
}

THUMBNAIL_ALIASES = {
    '': {
        'share': {'size': (1200, 628), 'crop': True, 'upscale': True, 'quality': 75},
        'filter': {'size': (30, 40), 'crop': True, 'upscale': True, 'quality': 75},
        'filter_big': {'size': (50, 65), 'crop': True, 'upscale': True, 'quality': 75},
        'mini': {'size': (180, 110), 'crop': True, 'upscale': True, 'quality': 75},
        'sq_xs': {'size': (110, 110), 'crop': True, 'upscale': True, 'quality': 75},
        'sq_sm': {'size': (768, 768), 'crop': True, 'upscale': True, 'quality': 75},
        'sq_md': {'size': (1024, 1024), 'crop': True, 'upscale': True, 'quality': 75},
        'sq_lg': {'size': (1280, 1280), 'crop': True, 'upscale': True, 'quality': 75},
        'hd_xs': {'size': (800, 450), 'crop': True, 'upscale': True, 'quality': 75},
        'hd_sm': {'size': (800, 450), 'crop': True, 'upscale': True, 'quality': 75},
        'hd_md': {'size': (1366, 768), 'crop': True, 'upscale': True, 'quality': 75},
        'hd_lg': {'size': (1920, 1080), 'crop': True, 'upscale': True, 'quality': 75},
    },
}
