# server/settings/base.py
from pathlib import Path
import os

from dotenv import load_dotenv
import urllib.parse as urlparse
from datetime import timedelta

load_dotenv()

TRIP_JOINING_PAGE = "https://plannder.com/trip/invite/"
LOGIN_PAGE = "https://plannder.com/login/"
FAILED_REGISTRATION_PAGE = "https://plannder.com/registration-failed/"

ASGI_APPLICATION = "server.asgi.application"

BASE_DIR = Path(__file__).resolve().parent.parent.parent

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
url = urlparse.urlparse(redis_url)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [str(os.environ.get("REDIS_URL")) + "?ssl_cert_reqs=none"],
        },
    },
}

# Application definition

INSTALLED_ADDITIONAL_APPS = [
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'sslserver',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
    'cloudinary',
    'cloudinary_storage',
    'django_extensions',
]

OWN_ADDITIONAL_APPS = [
    'dicts',
    'users',
    'permissions',
    'trips',
    'user_auth',
    'itineraries',
    'chats.apps.ChatsConfig',
    'channels',
    'payments',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + INSTALLED_ADDITIONAL_APPS + OWN_ADDITIONAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Redis server URL
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'server.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'BLACKLIST_AFTER_ROTATION': True,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Plannder API',
    'DESCRIPTION': 'Engineering thesis PJATK',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    "SECURITY": [{"BearerAuth": []}],
    "SWAGGER_UI_INIT_OVERRIDES": {
        "docExpansion": "none",
    },
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
        "displayRequestDuration": True,
    },
    'REDOC_DIST': 'SIDECAR',
    'DISABLE_DEFAULT_SCHEMA_GROUPING': True,
    'COMPONENT_SPLIT_REQUEST': True,
    'FILTER_INSPECTORS': [
        'drf_spectacular.contrib.django_filters.DjangoFilterInspector',
    ],
    'TAGS': [
        {'name': 'trip', 'description': 'Endpoints for managing trips.'},
        {'name': 'ticket', 'description': 'Endpoints for managing tickets.'},
        {'name': 'expense', 'description': 'Endpoints for managing expenses.'},
        {'name': 'itinerary', 'description': 'Endpoints for managing itineraries.'},
        {'name': 'itinerary activity', 'description': 'Endpoints for managing itinerary activities.'},
    ],
}

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

# Email config

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST = os.environ.get('EMAIL_HOST')

# Internationalization

LANGUAGE_CODE = 'pl'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True



# Auth

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = 'user_auth/login/'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cookies security settings

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media settings
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'https://localhost.com').split(',')
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'https://plannder.com').split(',')
CSRF_TRUSTED_ORIGINS = [
    "https://api.plannder.com"
]

# Stripe config

STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', "sk_test_your_key")
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', "pk_test_your_key")
STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET', "whsec_your_key")
