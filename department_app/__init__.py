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

import os

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

api = Api(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=MIGRATION_DIR)

from .rest import init_api
init_api()

from .views import init_views
init_views()

from .models import department, employee
