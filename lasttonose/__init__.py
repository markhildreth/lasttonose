from flask import Flask, app, request, redirect, abort, url_for
app = Flask(__name__)

# Set up the database
from lasttonose.data import init as init_database
init_database()

# Lastly, import the views (so that their routes are configured)
import lasttonose.views


