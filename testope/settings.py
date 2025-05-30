
from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _
import json
import getpass
from django.urls import reverse, reverse_lazy
import tempfile
from django.conf import global_settings





BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-f&w(w!!zuontbinw7=m--*ymy$mc^o_&^-%tqoaodb=s@_mom0'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplicaciones personalizadas
    'applications.home',
    'applications.learning',
    'applications.social',
    'applications.assistant',

    #recaptcha
    'django_recaptcha',

    # Allauth UI
    'allauth_ui',
    # Django-Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', 

    
    'widget_tweaks',
    'slippers',

    # Otros paquetess
    'rosetta',
    'normalize',
    'channels',
]

ALLAUTH_UI_THEME = "light"

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]


ROOT_URLCONF = 'testope.urls'

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

WSGI_APPLICATION = 'testope.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




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

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_TZ = True
LANGUAGES = (
    ('es', _('Spanish')),
    #('en', _('English')),
    #('ca', _('Catalan')),
    ('eu', _('Basque')),

)
PARLER_LANGUAGES = {
    None: (
        {'code': 'es', },  # Spanish
        #{'code': 'en', },  # English
        #{'code': 'ca', },  # Catalan
        {'code': 'eu', },  # Basque
    ),
    'default': {
        'fallbacks': ['es'],
        'hide_untranslated': False,
    }
}


LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'project_locale'),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    "/var/www/static/",
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LOGOUT_REDIRECT_URL = 'home_app:home'
LOGIN_REDIRECT_URL = 'home_app:home'

# Configuración de Email en Django
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # Servidor SMTP de Gmail (cambia si usas otro servicio)
EMAIL_PORT = 587  # Puerto SMTP
EMAIL_USE_TLS = True  # Habilita TLS (seguro)
EMAIL_HOST_USER = "euskodev@gmail.com"  # Tu dirección de correo
EMAIL_HOST_PASSWORD = "Euskodev34123412!"  # Tu contraseña (mejor usar variables de entorno)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Correo por defecto para enviar


RECAPTCHA_PUBLIC_KEY = "6Ld-Td4qAAAAABFa0JgDzvoJhu9kswUuwbAT41NZ"
RECAPTCHA_PRIVATE_KEY = "6Ld-Td4qAAAAAF0oEfprhPS-RxGeQLlD4eUJAQFK"

