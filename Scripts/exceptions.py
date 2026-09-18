'''Module containing custom exceptions.'''

class NoMatchError(Exception):
    '''Raises error when no case pattern is matched.'''
    def __init__(self, _) -> None:  # noqa: D107
        super().__init__(f"{_} doesn't match any case pattern.")
