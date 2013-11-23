def get_game_state(game):
    still_playing = [x for x in game.participants if not x.touched_nose]

    if len(still_playing) == 1:
        return ParticipantLostGameState(still_playing[0].name)
    else:
        return TBDGameState()
        
class ParticipantLostGameState(object):
    def __init__(self, loser):
        self.loser = loser
        self.game_over = True

class TBDGameState(object):
    def __init__(self):
        self.game_over = False
