import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = 'dummy-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'mart.apps.MartConfig',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'etools': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_etools.sqlite3'),
    }
}

# ETL settings
ETL_PARALLEL_WORKERS = 4
ETL_IGNORE_ERRORS = False

# Stub multi-tenant methods
from django.db import connections
class Country:
    def __init__(self, name, schema_name):
        self.name = name
        self.schema_name = schema_name

connections['etools'].get_tenants = lambda: [Country('Lebanon','lebanon'), Country('Bolivia','bolivia')]
connections['etools'].set_schemas = lambda schemas: None

# Other minimal settings
ROOT_URLCONF = 'mart_project.urls'
WSGI_APPLICATION = 'mart_project.wsgi.application'
MIDDLEWARE = []
TEMPLATES = []