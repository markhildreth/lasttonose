from flask import Flask, app, request, redirect, abort, url_for

app = Flask(__name__)

app.config['IMAGE_COUNT'] = 6

# Set up the database
from lasttonose.data import db
db.init_app(app)

# Lastly, import the views (so that their routes are configured)
import lasttonose.views

