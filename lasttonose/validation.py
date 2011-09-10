class Validation(object):
    @staticmethod
    def SUCCESSFUL():
        return Validation()

    def __init__(self, errors=None):
        self.errors = errors or []

    @property
    def is_valid(self):
        return len(self.errors) == 0

def validate_creation(name, participants):
    errors = []

    if len(name.strip()) == 0:
        errors.append('You must input a game name')

    if len(participants) < 3:
        errors.append('You must have at least three participants')

    return Validation(errors=errors)

