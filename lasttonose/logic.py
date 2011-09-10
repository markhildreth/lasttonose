def get_game_state(game):
    not_touched_names = [name for name, participant in game['participants'].items() if participant['touched_nose'] == False]

    if len(not_touched_names) == 1:
        return ParticipantLostGameState(not_touched_names[0])
    else:
        return TBDGameState()
        
class ParticipantLostGameState(object):
    def __init__(self, loser):
        self.loser = loser
        self.game_over = True

class TBDGameState(object):
    def __init__(self):
        self.game_over = False
