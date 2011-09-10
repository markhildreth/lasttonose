from urllib import urlencode

from lasttonose import app, request, redirect, abort, url_for
from lasttonose import templating
from lasttonose.data import database, GameNotFound
from lasttonose import validation
from lasttonose import logic

@app.route('/', methods=['GET'])
def index():
    return templating.render('/index.mako')

def _render_creation_form(name='', participants=None, errors=None):
    # Create a participant list of at least 20 participants
    participants = participants or []
    participants = participants + ([''] * min(0, 20 - len(participants)))
    context = {
        'name' : name,
        'participants' : participants or [''] * 20,
    }
    return templating.render('/create.mako', context)

def _url_for_game_intro(game):
    return '/game_intro/' + str(game['_id'])

def _url_for_game(game):
    return '/game/' + str(game['_id'])

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return _render_creation_form()

    if request.method == 'POST':
        name = request.form['last_to_nose_game_name']
        participants = set()
        for key, value in request.form.items():
            if key.startswith('last_to_nose_participant_') and value != '':
                participants.add(value)

        results = validation.validate_creation(name, list(participants))
        if results.is_valid:
            game = database.create_game(name, participants)

            game_created_url = url_for('game_created', game_id=str(game['_id']))
            return redirect(game_created_url)
        else:
            return _render_creation_form(name, participants, results.errors)
            
@app.route('/game_created/<game_id>')
def game_created(game_id):
    try:
        game = database.get_game(game_id)
    except GameNotFound as ex:
        abort(404, 'This game is not found')

    context = {
        'game' : game,
        'encoded_path' : _url_for_game_intro(game),
    }
    return templating.render('/game_created.mako', context)

@app.route('/game_intro/<game_id>')
def game_intro(game_id):
    try:
        game = database.get_game(game_id)
    except GameNotFound as ex:
        abort(404, 'This game is not found')

    context = {
        'game' : game,
    }
    return templating.render('/game_intro.mako', dict(game=game))

@app.route('/game/<game_id>')
def game(game_id):
    try:
        game = database.get_game(game_id)
    except GameNotFound as ex:
        abort(404, 'This game is not found')

    context = {
        'game' : game,
    }

    game_state = logic.get_game_state(game)
    return templating.render('/game.mako', dict(game=game, game_state=game_state))


@app.route('/touch_nose', methods=['POST'])
def touch_nose():
    game_id = request.form['game']
    participant_name = request.form['participant']

    try:
        game = database.get_game(game_id)
    except GameNotFound as ex:
        abort(404, 'This game is not found')

    participants = [x for x in game['participants'] if x['name'] == participant_name]
    if len(participants) == 0:
        abort(500, 'Participant not found')
    elif len(participants) ==1:
        participant = participants[0]
        participant['touched_nose'] = True
        database.update_game(game)
        return redirect(_url_for_game(game))

