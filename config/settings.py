from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-qop7c%d_8b@f=)m!8lwpir-j#pc(-&7292yk(hvm!gt*id7*tf'

DEBUG = True

ALLOWED_HOSTS = []


# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'EntrepriseApp',
    'ExpeditionApp',
    'OffreApp',
    'VehiculeApp',
]


# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Configuration des URL
ROOT_URLCONF = 'config.urls'


# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Application WSGI
WSGI_APPLICATION = 'config.wsgi.application'


# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'mariem.sqlite3',
    }
}


# Validation des mots de passe
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


# Langue et fuseau horaire
LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Africa/Tunis'

USE_I18N = True

USE_TZ = True


# Fichiers statiques
STATIC_URL = 'static/'


# Clé primaire par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Modèle utilisateur personnalisé
AUTH_USER_MODEL = 'EntrepriseApp.Utilisateur'
