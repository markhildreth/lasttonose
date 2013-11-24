import random
from urllib import quote

from flask import request, redirect, abort, url_for, render_template

from . import app, db
from .models import Game, Participant
from .forms import CreateGameForm

@app.route('/', methods=['GET'])
def index():
    return render_template('/index.html')

def _quote_game_name(game_name):
    game_name = game_name.lower().replace(' ', '-')
    acceptable_characters = 'abcdefghijklmnopqrstuvwxyz0123456789-._~'
    return ''.join([x for x in game_name if x in acceptable_characters])

def _url_for_game_intro(game):
    return url_for('game', game_id=game.id, game_description=_quote_game_name(game.name), _external=True)

def _url_for_game(game):
    return url_for('game_results', game_id=game.id, game_description=_quote_game_name(game.name))

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateGameForm()

    if form.validate_on_submit() and form.run():
        return redirect(url_for('game_created', game_id=form.game.id))

    return render_template('/create.html', form=form)
            
@app.route('/game_created/<int:game_id>')
def game_created(game_id):
    game = Game.query.get_or_404(game_id)

    context = {
        'game' : game,
        'game_url' : _url_for_game_intro(game),
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

