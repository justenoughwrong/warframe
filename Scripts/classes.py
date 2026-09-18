from dataclasses import dataclass
from typing import ReadOnly

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
