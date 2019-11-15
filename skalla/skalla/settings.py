"""
Django settings for skalla project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
from decouple import config
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [config('ALLOWED_HOSTS')]


## Application definition
#SHARED_APPS = [
#    'core'
#]


INSTALLED_APPS = [
    # 'tenant_schemas',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'web',
    'api',
    'core',
    'empresa',
    'cliente'
    # 'teste'
]


#TENANT_APPS = ['teste']

# TENANT_MODEL = 'core.model.ClienteSistema'

# DEFAULT_FILE_STORAGE = 'core.model.ClienteSistema'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# MIDDLEWARE_CLASSES = (
#    'tenant_schemas.middleware.TenantMiddleware',
# )

# DATABASE_ROUTERS = (
#    'tenant_schemas.routers.TenantSyncRouter',
# )


ROOT_URLCONF = 'skalla.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'DIRS': [],
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

WSGI_APPLICATION = 'skalla.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {

    'default': {
        'ENGINE': config('DATABASE_ENGINE'),
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),  # 8000 is default
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.BasicAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    #     #'rest_framework.authentication.TokenAuthentication',
    #     'rest_framework_simplejwt.authentication.JWTAuthentication'
    # ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ('*')
CORS_ALLOW_HEADERS = ('*')

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'SkAlla',
    'HEADER_DATE_FORMAT': 'l, j F Y',
    #'HEADER_TIME_FORMAT': 'H:i',

    # forms
    # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    # 'MENU_ICONS': {
    #    'sites': 'icon-leaf',
    #    'auth': 'icon-lock',
    # },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    # 'MENU_EXCLUDE': ('auth.group',),
    'MENU': (
        'sites',
        {
            'label': 'Minhas Escalas',
            'icon':'icon-list',
            'url': '/minhaescala/'
        },
        {
            'label': 'Imprimir Escalas',
            'icon':'icon-list',
            'url': '/imprimirescalas/'
        },
        {
            'label': 'Solicitações',
            'icon':'icon-envelope',
            'url': '/solicitacoes/'
        },
{
            'label': 'Escalas',
            'icon':'icon-calendar',
            'url': '/escalas/'
        },
        {
            'label':'Empresa' ,
            'icon':'icon-lock',
            'models': ('empresa.Empresa','empresa.Colaborador','empresa.Area','empresa.Departamento')
        },
        {
            'label':'Clientes' ,
            'icon':'icon-lock',
            'models': ('cliente.Cliente','cliente.PontoAlocacao','cliente.Turno')
        },
        {
            'label': 'Configurações',
            'icon':'icon-cog',
            'models': ('cliente.PerfilJornada','cliente.Turno','auth.user', 'auth.group', 'core.Configuracao', 'core.Cidade','core.Estado','core.Pais')
        },
        {
            'label': 'DESENVOLVIMENTO',
            'icon':'icon-cog',
            'models': ('cliente.Escala','cliente.EscalaColaborador')
        },
    ),

    # misc
    # 'LIST_PER_PAGE': 15
}
