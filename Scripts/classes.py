'''Script to contain dataclasses representing database tables.'''

from dataclasses import dataclass


@dataclass
class User:
    '''testing.'''
    name: str
    id: int = None

@dataclass
class Warframe:
    '''testing.'''
    name: str
    id: int = None
