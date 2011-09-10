from pymongo import Connection
from bson.objectid import ObjectId

database = None

def init():
    global database
    database = Database()

class Database(object):
    def __init__(self):
        self.connection = Connection()
        self.db = self.connection.lasttonose
        self.games = self.db.games

    def create_game(self, name, participants):
        game = {'name' : name, 'participants' : []}
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
