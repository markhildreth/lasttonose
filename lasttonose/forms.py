import wtforms as wtf
from wtforms import validators as v
from flask.ext.wtf import Form

from . import db
from .models import Game, Participant

class CreateGameForm(Form):
    name = wtf.TextField('name', validators=[v.DataRequired()])
    participants = wtf.FieldList(
            wtf.TextField('participant_name', validators=[]),
            min_entries=20, max_entries=20
    )

    def validate_participants(self, field):
        # Retrieve the participant names that were not left empty.
        self.participant_names = [x for x in field.data if x.strip()]

        if len(self.participant_names) < 3:
            raise wtf.ValidationError(u'You must have at least three participants')

    def run(self):
        name = self.name.data.strip('.').strip('!') # Don't need no punctuation.

        self.game = Game(name=name)
        for participant_name in self.participant_names:
            self.game.participants.append( Participant(name=participant_name) )
        db.session.add(self.game)
        
        try:
            db.session.commit()
            return True
        except Exception as e:
            self.misc_errors = [unicode(e)]
            return False

