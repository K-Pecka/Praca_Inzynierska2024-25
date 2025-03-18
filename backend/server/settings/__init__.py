import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "development":
    from .development import *
