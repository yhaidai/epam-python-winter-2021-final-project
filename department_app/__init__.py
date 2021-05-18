import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# fix of an issue: https://github.com/flask-restful/flask-restful/pull/913
import flask.scaffold

flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
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
