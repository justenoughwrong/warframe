'''Script to contain dataclasses representing database tables.'''

from dataclasses import dataclass


@dataclass
class User:
    '''User data model.

    Attributes:
        id: Unique identifier.
        name: user's name.
    '''
    name: str
    id: int = None

@dataclass
class Warframe:
    '''Warframe data model.

    Attributes:
        id: Unique identifier.
        name: warframe's name.
    '''
    name: str
    id: int = None
