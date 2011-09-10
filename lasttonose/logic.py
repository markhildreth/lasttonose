def get_game_state(game):
    not_touched = [x for x in game['participants'] if x['touched_nose'] == False]

    if len(not_touched) == 1:
        return ParticipantLostGameState(not_touched[0]['name'])
    else:
        return TBDGameState()
        
class ParticipantLostGameState(object):
    def __init__(self, loser):
        self.loser = loser
        self.game_over = True

class TBDGameState(object):
    def __init__(self):
        self.game_over = False
