import random
from urllib import quote

from flask import request, redirect, abort, url_for, render_template

from . import app, validation, logic, get_current_image_count
from .data import database, GameNotFound

@app.route('/', methods=['GET'])
def index():
    return render_template('/index.html')

def _render_creation_form(name='', participants=None, errors=None):
    # Create a participant list of at least 20 participants
    participants = participants or []
    participants = list(participants) + ([''] * max(0, 20 - len(participants)))
    context = {
        'name' : name,
        'participants' : enumerate(participants or [''] * 20),
        'errors' : errors or [],
    }
    return render_template('/create.html', **context)

def _quote_game_name(game_name):
    game_name = game_name.lower().replace(' ', '-')
    acceptable_characters = 'abcdefghijklmnopqrstuvwxyz0123456789-._~'
    return ''.join([x for x in game_name if x in acceptable_characters])

def _url_for_game_intro(game):
    return '/' + str(game['id']) + '/' + _quote_game_name(game['name'])

def _url_for_game(game):
    return '/game_results/' + str(game['id']) + '/' + _quote_game_name(game['name'])

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return _render_creation_form()

    if request.method == 'POST':
        name = request.form['last_to_nose_game_name']
        name = name.strip('.').strip('!') # Don't need no punctuation.
        participants = set()
        for key, value in request.form.items():
            if key.startswith('last_to_nose_participant_') and value.strip() != '':
                participants.add(value)

        results = validation.validate_creation(name, list(participants))
        if results.is_valid:
            game = database.create_game(name, participants)

            game_created_url = url_for('game_created', game_id=str(game['id']))
            return redirect(game_created_url)
        else:
            return _render_creation_form(name, participants, results.errors)
            
@app.route('/game_created/<int:game_id>')
def game_created(game_id):
    try:
        game = database.get_game(game_id)
    except GameNotFound as ex:
        abort(404, 'This game is not found')

    context = {
        'game' : game,
        'encoded_path' : _url_for_game_intro(game),
    }
    return render_template('/game_created.html', **context)

@app.route('/<int:game_id>')
@app.route('/<int:game_id>/<string:game_description>')
def game(game_id, game_description=None):
    try:
        game = database.get_game(game_id)
    except GameNotFound as ex:
        abort(404, 'This game is not found')

    if _quote_game_name(game['name']) != game_description:
        return redirect(_url_for_game_intro(game))

    # Sort participants by their name
    participants = sorted(game['participants'].items())
    context = {
        'game_id' : game['id'],
        'game_name' : game['name'],
        'participants' : participants,

    }
    return render_template('/game.html', **context)


@app.route('/game_results/<int:game_id>')
@app.route('/game_results/<int:game_id>/<string:game_description>')
def game_results(game_id, game_description=None):
    try:
        game = database.get_game(game_id)
    except GameNotFound as ex:
        abort(404, 'This game is not found')

    if _quote_game_name(game['name']) != game_description:
        return redirect(_url_for_game(game))

    image_count = app.config['IMAGE_COUNT']

    try:
        # Try to get a sample of images, so there are no duplicates...
        participant_image_numbers = random.sample(range(1, image_count), len(game['participants']))
    except ValueError:
        # More players than images. Just get random images.
        participant_image_numbers = [random.randint(1, image_count) for x in range(len(game['participants']))]

    # Sort participants by their name
    participants = sorted(game['participants'].items())

    game_state = logic.get_game_state(game)

    print participants
    context = {
        'game_name' : game['name'],
        'participants' : zip(participants, participant_image_numbers),
        'game_state' : game_state,
    }

    return render_template('/game_results.html', **context)


@app.route('/touch_nose', methods=['POST'])
def touch_nose():
    game_id = int(request.form['game'])
    participant_name = request.form['participant']

    try:
        game = database.get_game(game_id)
    except GameNotFound as ex:
        abort(404, 'This game is not found')

    if not logic.get_game_state(game).game_over:
        participants = [participant for name, participant in game['participants'].items() if name == participant_name]
        participant = participants[0]
        participant['touched_nose'] = True
        database.update_game(game)

    return redirect(_url_for_game(game))

