import psycopg2
import dj_database_url

from .base import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

API_URL = 'https://api.plannder.com'

# API access settings

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'plannder.com',
    'api.plannder.com',
    'www.plannder.com',
]

CORS_ALLOWED_ORIGINS = [
    "https://localhost.com",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
    "https://127.0.0.1:8000",
    'https://www.plannder.com',
    'https://api.plannder.com',
]

# Database config

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)
}

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
