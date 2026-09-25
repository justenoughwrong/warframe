'''Module containing custom exceptions.'''


class NoMatchError(Exception):
    '''No case pattern match found.'''
    def __init__(self, case_pattern: str | int) -> None:  # noqa: D107
        super().__init__(f"{case_pattern} doesn't match any case pattern.")

class NotIterableError(TypeError):
    '''Arg type is not iterable.'''
    def __init__(self, _) -> None:  # noqa: D107
        super().__init__(f'{_} must be iterable.')

class NotFoundError(TypeError):
    '''Base for not found exceptions.'''
    def __init__(self, _: str | int) -> None:  # noqa: D107
        super().__init__(f'{_} not found.')

class UserNotFoundError(NotFoundError):
    '''User not found.'''
    def __init__(self, _) -> None:  # noqa: D107
        super().__init__(f'{_} user')

class WarframeNotFoundError(NotFoundError):
    '''Warframe not found.'''
    def __init__(self, _) -> None:  # noqa: D107
        super().__init__(f'{_} warframe')
