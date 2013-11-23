from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    participants = db.relationship('Participant',
            order_by='Participant.name',
            lazy='joined')

    @property
    def is_game_over(self):
        return self.loser != None

    @property
    def loser(self):
        untouched = [x for x in self.participants if not x.touched_nose]
        if len(untouched) == 1:
            return untouched[0]

        return None

class Participant(db.Model):
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    name = db.Column(db.Text)
    touched_nose = db.Column(db.Boolean)
    
