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
    return Validation.SUCCESSFUL()
