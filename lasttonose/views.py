import random
from urllib import quote

from flask import request, redirect, abort, url_for, render_template

from . import app, db
from .validation import validate_creation
from .models import Game, Participant

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
    return url_for('game', game_id=game.id, game_description=_quote_game_name(game.name))

def _url_for_game(game):
    return url_for('game_results', game_id=game.id, game_description=_quote_game_name(game.name))

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

        results = validate_creation(name, list(participants))
        if results.is_valid:
            game = Game(name=name)
            for participant_name in participants:
                game.participants.append( Participant(name=participant_name) )
            db.session.add(game)
            db.session.commit()

            game_created_url = url_for('game_created', game_id=str(game.id))
            return redirect(game_created_url)
        else:
            return _render_creation_form(name, participants, results.errors)
            
@app.route('/game_created/<int:game_id>')
def game_created(game_id):
    game = Game.query.get_or_404(game_id)

    context = {
        'game' : game,
        'encoded_path' : _url_for_game_intro(game),
    }
    return render_template('/game_created.html', **context)

@app.route('/<int:game_id>')
@app.route('/<int:game_id>/<string:game_description>')
def game(game_id, game_description=None):
    game = Game.query.get_or_404(game_id)

    if _quote_game_name(game.name) != game_description:
        return redirect(_url_for_game_intro(game))

    context = {
        'game' : game,
    }
    return render_template('/game.html', **context)


@app.route('/game_results/<int:game_id>')
@app.route('/game_results/<int:game_id>/<string:game_description>')
def game_results(game_id, game_description=None):
    game = Game.query.get_or_404(game_id)

    if _quote_game_name(game.name) != game_description:
        return redirect(_url_for_game(game))

    image_count = app.config['IMAGE_COUNT']

    try:
        # Try to get a sample of images, so there are no duplicates...
        participant_image_numbers = random.sample(range(1, image_count), len(game.participants))
    except ValueError:
        # More players than images. Just get random images.
        participant_image_numbers = [random.randint(1, image_count) for x in range(game.participants)]

    context = {
        'game' : game,
        'participants' : zip(game.participants, participant_image_numbers),
    }

    return render_template('/game_results.html', **context)


@app.route('/touch_nose', methods=['POST'])
def touch_nose():
    game_id = int(request.form['game'])
    participant_name = request.form['participant']

    game = Game.query.get_or_404(game_id)

    if not game.is_game_over:
        participant = [x for x in game.participants if x.name == participant_name][0]
        participant.touched_nose = True
        db.session.commit()

    return redirect(_url_for_game(game))

