"""
    the flask configuration file
"""

import os

CONTEXT_DIR = os.path.abspath(os.path.dirname(__file__))

POSTGRES = {
    'user': 'postgres',
    'pw': 'Sharon0108',     # modify this line to match your db password
    'db': 'recipe',
    'host': 'localhost',
    'port': '5432',         # modify this line to your default port - 5432
}

SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
SQLALCHEMY_TRACK_MODIFICATIONS = True

CSRF_ENABLED = True
SECRET_KEY = 'password'