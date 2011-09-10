import os
import random

from pymongo import Connection
from pymongo.son import SON
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
        self.game_ids = self.db.game_id

    def _create_new_id(self):
        args = {
            'query' : {'_id' : 'manager'},
            'update' : {'$inc' : {'next_id' : 1} },
            'upsert' : True,
        }
        manager = self.game_ids.find_and_modify(**args)
        return manager.get('next_id', 0)

    def create_game(self, name, participant_names):
        game = {'name' : name, 'participants' : {}}
        participants = game['participants']

        current_image_count = _get_current_image_count()
        game['start_image_count'] = current_image_count
        random.seed()
        game['random_seed'] = random.random()

        for participant_name in participant_names:
            participants[participant_name] = {'touched_nose' : False}

        game['id'] = self._create_new_id()

        self.games.insert(game)
        return game

    def get_game(self, game_id):
        game = self.games.find_one({'id' : game_id})

        if game == None:
            raise GameNotFound()

        return game

    def update_game(self, game):
        self.games.save(game)

class GameNotFound(Exception):
    pass
