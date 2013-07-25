# email settings
EMAIL_ALERT_RECIPIENTS = ['max_fowler@brown.edu']   # controls who receives email alerts about scripts progress by default
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'maximusfowler@gmail.com'
EMAIL_HOST_PASSWORD = 'bjxdyhpmmlwolklc'
DEFAULT_FROM_EMAIL = 'maximusfowler@gmail.com'

import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
INSTALLED_APPS = ('longscripts')
SECRET_KEY = "tbi3=9_@f(l6666sdtvly9jkkkk1m!kjursdk62#_b6_(x9d1b"
GLOBAL = {}

# db orm
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'test.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        },
    }

