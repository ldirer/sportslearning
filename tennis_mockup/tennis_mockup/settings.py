"""
Django settings for tennis_mockup project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print BASE_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    with file(os.path.join(BASE_DIR, 'tennis_mockup/secret_key.txt')) as f:
        SECRET_KEY = f.read()

    with file(os.path.join(BASE_DIR, 'tennis_mockup/secret_mail')) as f:
        MAIL_PW = f.read()

    with file(os.path.join(BASE_DIR, 'tennis_mockup/secret_db')) as f:
        SECRET_DB = f.read()
except IOError:
    SECRET_KEY = os.environ['SPORTSLEARNING_SECRET_KEY']
    MAIL_PW = os.environ['SPORTSLEARNING_SECRET_MAIL']
    SECRET_DB = os.environ['SPORTSLEARNING_SECRET_DB']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
PRODUCTION = True
if PRODUCTION:
    DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.sportslearning.fr',
                 'sportslearning.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_nose',
    'tennis',
    'rest_framework',
    'pipeline',
    'django_extensions',
)

# if DEBUG and not PRODUCTION:
    #INSTALLED_APPS += ('debug_toolbar',)
if not DEBUG:
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'PAGINATE_BY': 10,
}


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# if DEBUG and not PRODUCTION:
#     MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'tennis_mockup.urls'

WSGI_APPLICATION = 'tennis_mockup.wsgi.application'

ADMINS = ()
MANAGERS = ADMINS
SEND_BROKEN_LINK_EMAILS = False
SERVER_EMAIL = 'server@sportslearning.com'

EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'laurent.direr@gmail.com'
EMAIL_HOST_PASSWORD = MAIL_PW

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tennis_web',
        'USER': 'laurent',
        'PASSWORD': SECRET_DB,
        'HOST': 'localhost',
        'PORT': ''
    }
}

# For Heroku
# Parse database configuration from $DATABASE_URL
if PRODUCTION:
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../static/')

#ADDED FOR TUTORIAL OPENCLASSROOMS
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "assets/"),
)

# For Heroku
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


#ADDED FOR TUTORIAL OPENCLASSROOMS
APPEND_SLASH = True

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates/"),
)

TEMPLATE_STRING_IF_INVALID = 'Unknown Variable Name'

LOGIN_REDIRECT_URL = '/tennis'

# FIXTURE_DIRS = (
#    '/home/laurent/Python/Django/tennis/fixtures/',
# )


#TODO: Assess if this is interesting to do in production.
#  #Added for pipeline asset manager.
# STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
# PIPELINE_CSS = {
#     'colors': {
#         'source_filenames': (
#           'css/core.css',
#           'css/colors/*.css',
#           'css/layers.css'
#         ),
#         'output_filename': 'css/colors.css',
#         'extra_context': {
#             'media': 'screen,projection',
#         },
#     },
# }
#
# PIPELINE_JS = {
#     'stats': {
#         'source_filenames': (
#           'js/jquery.js',
#           'js/d3.js',
#           'js/collections/*.js',
#           'js/application.js',
#         ),
#         'output_filename': 'js/stats.js',
#     }
# }

