# Make this unique, and don't share it with anybody.
SECRET_KEY = 'o#3)v@gq9c8afla4wetc)#gcr$sun7_2kw5*i!ch^(mwd@uy06'
# TODO: CHANGE IN PRODUCTION

DEBUG = True  # TODO: set to True for dev, False in production
TEMPLATE_DEBUG = DEBUG

DATABASES = {  # TODO
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sql',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
