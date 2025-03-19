import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "testr":
    from .test import *
else:
    from .development import *
