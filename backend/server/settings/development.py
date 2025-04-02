# server/settings/development.py

from .base import *


DEBUG = True

SECRET_KEY = 'LYLmGW3Eabxzn2kdQeFGumZflknV1aFQAlIamvbuAjw='

API_URL = 'https://127.0.0.1:8000'

# Database config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

<<<<<<< HEAD
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

=======
>>>>>>> afc59b9 (Delete useless templates, update settings, add .enc and profile, fix tests)
