from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

import os

app = Flask(__name__)

app.config['IMAGE_COUNT'] = 6
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

# Set up the database
from lasttonose.models import db
db.init_app(app)

migrate = Migrate(app, db)

# Lastly, import the views (so that their routes are configured)
import lasttonose.views

manager = Manager(app)
manager.add_command('db', MigrateCommand)
