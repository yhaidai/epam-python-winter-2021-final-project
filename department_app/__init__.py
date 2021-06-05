"""
Sources root package.

Initializes web application and web service, contains following subpackages and
modules:

Subpackages:

- `database`: contains modules used to populate database
- `migrations`: contains migration files used to manage database schema
- `models`: contains modules with Python classes describing database models
- `rest`: contains modules with RESTful service implementation
- `schemas`: contains modules with serialization/deserialization schemas for \
models
- `service`: contains modules with classes used to work with database
- `static`: contains web application static files (scripts, styles, images)
- `templates`: contains web application html templates
- `views`: contains modules with web controllers/views
- `tests`: contains modules with unit tests
"""

# pylint: disable=wrong-import-position, protected-access, cyclic-import
import logging.config
import os
import sys

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# fix of an issue: https://github.com/flask-restful/flask-restful/pull/913
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

# import order is crucial
from flask_restful import Api

from config import Config

MIGRATION_DIR = os.path.join('department_app', 'migrations')
TEMPLATES_DIR = 'templates'

app = Flask(__name__, template_folder=TEMPLATES_DIR)
app.config.from_object(Config)

# logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

file_handler = logging.FileHandler(filename='app.log', mode='w')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

# pylint: disable=no-member
logger = app.logger
logger.handlers.clear()
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.DEBUG)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.handlers.clear()
werkzeug_logger.addHandler(file_handler)
werkzeug_logger.addHandler(console_handler)
werkzeug_logger.setLevel(logging.DEBUG)

# sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
# sqlalchemy_logger.addHandler(file_handler)
# sqlalchemy_logger.addHandler(console_handler)
# sqlalchemy_logger.setLevel(logging.DEBUG)


# RESTful API
api = Api(app)

# database
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=MIGRATION_DIR)

from .rest import init_api
init_api()

from .views import init_views
init_views()

from .models import department, employee
