from pathlib import Path
from decouple import config
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Helper functions:
# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/
import boto3
import json
import os


def get_secret(secret_name):

    use_aws = os.getenv("USE_AWS_SECRETS", "false").lower() == "true"
    if not use_aws:
        # Return some mock secret data so app doesn’t break
        return {"secret_key": "local-dev-secret"}
    
    """
    Fetch a secret from AWS Secrets Manager.
    """
    region_name = os.getenv("AWS_REGION", "us-east-2")
    client = boto3.client('secretsmanager', region_name=region_name)
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = response['SecretString']
        return json.loads(secret)
    except Exception as e:
        raise Exception(f"Error fetching secret {secret_name}: {e}")

def get_env_variable(var_name, default=None):
    return os.getenv(var_name, default)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("alphacrm/secret_key")['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['3.146.34.38', 
                 'alphamminc.com', 
                 'www.alphamminc.com', 
                 'localhost', 
                 '127.0.0.1', 
                 'host.docker.internal',]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crm',
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alphacrm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'alphacrm.wsgi.application'


USE_AWS_SECRETS = get_env_variable("USE_AWS_SECRETS", "false").lower() == "true"

if not USE_AWS_SECRETS:
    # Local development settings
    EMAIL_HOST_USER = get_env_variable("EMAIL_HOST_USER", "fake@example.com")
    EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_HOST_PASSWORD", "fake-password")
    DEFAULT_FROM_EMAIL = get_env_variable("DEFAULT_FROM_EMAIL", "fake@example.com")

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": get_env_variable("DB_NAME", "my_local_db"),
            "USER": get_env_variable("DB_USER", "django_user"),
            "PASSWORD": get_env_variable("DB_PASSWORD", "django_password"),
            "HOST": get_env_variable("DB_HOST", "localhost"),
            "PORT": get_env_variable("DB_PORT", "3306"),
        }
    }
else:
    # production mode: pull from aws
    extra_secrets = get_secret("custom/extra-alpha-db-info")
    rds_secrets = get_secret("rds!db-b9127d9c-9291-40c6-b2f8-e13cd630d333")

    EMAIL_HOST_USER = extra_secrets['email_host_user']
    EMAIL_HOST_PASSWORD = extra_secrets['email_host_password']
    DEFAULT_FROM_EMAIL = extra_secrets['default_from_email']
    # Database
    # https://docs.djangoproject.com/en/5.1/ref/settings/#databases
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": extra_secrets["db_name"],
            "USER": rds_secrets["username"],
            "PASSWORD": rds_secrets["password"],
            "HOST": extra_secrets["db_host"],
            "PORT": extra_secrets["db_port"],
        }
    }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-2.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# URL to access static files
STATIC_URL = '/static/'

# Directory where collectstatic will store files
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Directories containing source static files
STATICFILES_DIRS = [  # Keep this for your source files
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CSRF_TRUSTED_ORIGINS = [
    'https://alphamminc.com',
    'https://www.alphamminc.com', 
]

USE_X_FORWARDED_HOST = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security Settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    # Disable HTTPS enforcement in development
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
