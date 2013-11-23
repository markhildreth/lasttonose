from flask import Flask, app, request, redirect, abort, url_for
app = Flask(__name__)

app.config['IMAGE_COUNT'] = 6

# Set up the database
from lasttonose.data import init as init_database
init_database()

def get_current_image_count():
    # TODO: Probably a better way to get this.
    module_directory = os.path.abspath(os.path.dirname(__file__))
    image_directory = os.path.join(module_directory, 'static', 'images')
    filenames = os.listdir(image_directory)
    return len(list([x for x in filenames if x.startswith('touched_nose_')]))

# Lastly, import the views (so that their routes are configured)
import lasttonose.views

