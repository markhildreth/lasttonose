import os
import random

from pymongo import Connection
from bson.objectid import ObjectId

database = None

def init():
    global database
    database = Database()

def _get_current_image_count():
    module_directory = os.path.abspath(os.path.dirname(__file__))
    image_directory = os.path.join(module_directory, 'static', 'images')
    filenames = os.listdir(image_directory)
    return len(list([x for x in filenames if x.startswith('touched_nose_')]))


class Database(object):
    def __init__(self):
        self.connection = Connection()
        self.db = self.connection.lasttonose
        self.games = self.db.games

    def create_game(self, name, participants):
        game = {'name' : name, 'participants' : []}

        current_image_count = _get_current_image_count()
        game['start_image_count'] = current_image_count
        random.seed()
        game['random_seed'] = random.random()

        for participant in participants:
            game['participants'].append({'name' : participant, 'touched_nose' : False})

        self.games.insert(game)
        return game

    def get_game(self, game_id):
        game = self.games.find_one({'_id' : ObjectId(game_id)})

        if game == None:
            raise GameNotFound()

        return game

    def update_game(self, game):
        self.games.save(game)

class GameNotFound(Exception):
    pass
