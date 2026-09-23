'''Module containing custom exceptions.'''


class NoMatchError(Exception):
    '''Raises error when no case pattern is matched.'''
    def __init__(self, case_pattern: str | int) -> None:  # noqa: D107
        super().__init__(f"{case_pattern} doesn't match any case pattern.")

class NotIterableError(TypeError):
    '''Raises error when arg type is not iterable.'''
    def __init__(self, _) -> None:  # noqa: D107
        super().__init__(f'{_} must be iterable.')
