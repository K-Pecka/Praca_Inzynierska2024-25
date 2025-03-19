# server/settings/development.py

from .base import *


DEBUG = True

SECRET_KEY = 'LYLmGW3Eabxzn2kdQeFGumZflknV1aFQAlIamvbuAjw='

API_URL = 'https://127.0.0.1:8000'

# API access settings

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS_ALLOWED_ORIGINS = [
    "https://localhost.com",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
    "https://127.0.0.1:8000",
    "https://api.plannder.com"
]

ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
    'localhost',
    'testserver',
]

# Database config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
