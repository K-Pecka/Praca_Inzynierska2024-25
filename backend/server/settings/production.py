import psycopg2
import dj_database_url

from .base import *

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

SECRET_KEY = os.environ.get('SECRET_KEY')

API_URL = 'https://api.plannder.com'

# Database config

DATABASE_URL = os.environ.get('DATABASE_URL', '')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
DATABASES = {'default': dj_database_url.config(conn_max_age=60,
                                               ssl_require=True,
                                               conn_health_checks=True)}
