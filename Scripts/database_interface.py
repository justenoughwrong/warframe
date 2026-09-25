'''TODO add docstring.'''

# Built-in Imports
import sqlite3
import types
from pathlib import Path
from types import NotImplementedType

# Custom Imports
import classes
from classes import User, Warframe
from exceptions import (
    NoMatchError,
    NotIterableError,
    UserNotFoundError,
    WarframeNotFoundError,
)

# Path Constants
BASE_DIR = Path(__file__).parent.parent
DATABASE = BASE_DIR / 'warframe.db'
WARFRAMES_LIST = BASE_DIR / 'InitData' / 'warframes.txt'
SQL_DIR = BASE_DIR / 'sql'
CREATE = SQL_DIR / 'create'
DELETE = SQL_DIR / 'delete'
INSERT = SQL_DIR / 'insert'
SELECT = SQL_DIR / 'select'
UPDATE = SQL_DIR / 'update'

# Database Column Constants
USER_NAME = 'user_name'
USER_ID = 'user_id'
WARFRAME_NAME = 'warframe_name'
WARFRAME_ID = 'warframe_id'


def create_singleton(_) -> tuple:
    '''Creates a singleton.'''
    try:
        len(_)
    except TypeError:
        return (_,)
    else:
        return _


def _tuple_to_singletons(combined_tuple: tuple) -> tuple:
    '''Breaks tuple into individual tuples for each element and returns the new tuple.

    Returns:
        Tuple of tupled values for SQL parameters.
    '''
    try:
        return tuple(
            (_,) for _ in combined_tuple
        )
    except TypeError as err:
        raise NotIterableError(combined_tuple) from err


def iter_check(_) -> bool:
    '''Returns true if arg is iterable.'''
    try:
        len(_)
    except TypeError:
        return False
    else:
        return True


def get_type(_) -> type:
    '''Returns type of arg or arg[0].'''
    if iter_check(_):
        return type(_[0])
    return type(_)


def tuple_names(
    data_objects:
        tuple[User] |
        tuple[Warframe] |
        tuple[NotImplementedType] |
        User |
        Warframe |
        NotImplementedType) -> tuple:
    '''Return a tuple of names from dataclass objects.'''
    data_objects = create_singleton(data_objects)
    return tuple(
        _.name for _ in data_objects
    )


def tuple_ids(
    data_objects:
        tuple[User] |
        tuple[Warframe] |
        tuple[NotImplementedType] |
        User |
        Warframe |
        NotImplementedType) -> tuple:
    '''Return a tuple of ids from dataclass objects.'''
    data_objects = create_singleton(data_objects)
    return tuple(
        _.id for _ in data_objects
    )


def set_ids(
    data_objects:
        tuple[User] |
        tuple[Warframe] |
        tuple[NotImplementedType] |
        User |
        Warframe |
        NotImplementedType) -> None:
    '''Queries database for ids that match the dataclass object. Tables searched are determined by dataclass object type. Sets id for each dataclass object.'''
    data_objects = create_singleton(data_objects)
    data_type = get_type(data_objects)
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        match data_type:
            case classes.User:
                sql = Path(SELECT / 'user_id_by_name.sql').read_text()
                for user in data_objects:
                    params = {USER_NAME: user.name}
                    result = db.execute(sql, params).fetchone()
                    try:
                        user.id = result[USER_ID]
                    except TypeError as _:
                        raise UserNotFoundError(user) from _
            case classes.Warframe:
                sql = Path(SELECT / 'warframe_id_by_name.sql').read_text()
                for warframe in data_objects:
                    params = {WARFRAME_NAME: warframe.name}
                    result = db.execute(sql, params).fetchone()
                    try:
                        warframe.id = result[WARFRAME_ID]
                    except TypeError as _:
                        raise WarframeNotFoundError(warframe) from _
            case types.NotImplementedType:
                raise NotImplementedError
            case _:
                raise NoMatchError(data_type)


def get_all(table: str) -> tuple:
    '''Retrieves name every row in the matching table. Names are stored in dataclass objects of a corresponding type to the table.

    Args:
        table: String representing the table to fetch from.

    Returns:
        Tuple of dataclass objects containing the corresponding names.
    '''
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        match table:
            case 'users':
                query = Path(SELECT / 'user_names.sql').read_text()
                results = db.execute(query).fetchall()
                return tuple(
                    User(row[USER_NAME]) for row in results
                )
            case 'warframes':
                query = Path(SELECT / 'warframe_names.sql').read_text()
                results = db.execute(query).fetchall()
                return tuple(
                    Warframe(row[WARFRAME_NAME]) for row in results
                )
            case _:
                raise NoMatchError(table)

# only returns all of a user's _
def get_from_user(user: User, table: str) -> tuple:
    '''Queries the user lookup table that matches the table arg. Filters results based on the name of the user.

    Args:
        user: Dataclass object that contains the user name. Used to filter the database query.
        table: String representing the table joined by the lookup table.

    Returns:
        Tuple of dataclass objects matching the query results.
    '''
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        params = {USER_NAME: user.name}
        match table:
            case 'warframes':
                query = Path(SELECT / 'warframes_from_user.sql').read_text()
                results = db.execute(query, params).fetchall()
                return tuple(
                    Warframe(row[WARFRAME_NAME]) for row in results
                )
            case 'weapons':
                raise NotImplementedError
            case _:
                raise NoMatchError(table)

# only returns all users of _
def get_users_of(
    data_object:
        Warframe |
        NotImplementedType) -> tuple:
    '''Queries the user lookup table that matches arg's type. Filters results based on the name of the dataclass object.

    Args:
        data_object: Dataclass object that contains the name used to filter the database query.

    Returns:
        Tuple of User objects matching the query results.
    '''
    data_type = get_type(data_object)
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        match data_type:
            case classes.Warframe:
                query = Path(SELECT / 'users_of_warframe.sql').read_text()
                params = {WARFRAME_NAME: data_object.name}
            case types.NotImplementedType:
                raise NotImplementedError
            case _:
                raise NoMatchError(data_type)
        results = db.execute(query, params).fetchall()
        return tuple(
            User(row[USER_NAME]) for row in results
        )

# DATABASE ALTERING

def add(
    data_objects:
        tuple[User] |
        tuple[Warframe] |
        tuple[NotImplementedType] |
        User |
        Warframe |
        NotImplementedType) -> None:
    '''Inserts arg's name values into the database. Table is determined by the arg's type. Saves the changes.

    Args:
        data_objects: Dataclass objects containing the values to insert.
    '''
    data_type = get_type(data_objects)
    with sqlite3.connect(DATABASE) as db:
        match data_type:
            case classes.User:
                sql = Path(INSERT / 'user.sql').read_text()
            case classes.Warframe:
                sql = Path(INSERT / 'warframe.sql').read_text()
            case types.NotImplementedType:
                raise NotImplementedError
            case _:
                raise NoMatchError(data_type)
        params = _tuple_to_singletons(tuple_names(data_objects))
        db.executemany(sql, params)
        db.commit()


def add_to_user(
    user: User,
    data_objects:
        tuple[Warframe] |
        tuple[NotImplementedType] |
        Warframe |
        NotImplementedType) -> None:
    '''Inserts rows into user lookup table matching the table arg. Saves the changes.

    Args:
        user: User object of the user being added to.
        data_objects: Dataclass objects being added to the user lookup table.
    '''
    set_ids(user)
    set_ids(data_objects)
    data_objects = create_singleton(data_objects)
    data_type = get_type(data_objects)
    with sqlite3.connect(DATABASE) as db:
        match data_type:
            case classes.Warframe:
                sql = Path(INSERT / 'warframe_into_user.sql').read_text()
                params = tuple(
                    {USER_ID: user.id, WARFRAME_ID: _.id} for _ in data_objects
                )
            case types.NotImplementedType:
                raise NotImplementedError
            case _:
                raise NoMatchError(data_type)
        db.executemany(sql, params)
        db.commit()


def delete(
    data_objects:
        tuple[User] |
        tuple[Warframe] |
        tuple[NotImplementedType] |
        User |
        Warframe |
        NotImplementedType) -> None:
    '''Deletes rows from database that match dataclass objects.

    Args:
        data_objects: Dataclass objects being deleted from table.
    '''
    data_type = get_type(data_objects)
    with sqlite3.connect(DATABASE) as db:
        match data_type:
            case classes.User:
                sql = Path(DELETE / 'user.sql').read_text()
            case classes.Warframe:
                pass
            case types.NotImplementedType:
                raise NotImplementedError
            case _:
                raise NoMatchError(data_type)
        params = _tuple_to_singletons(tuple_names(data_objects))
        db.executemany(sql, params)
        db.commit()


def delete_from_users(
    data_objects:
        tuple[Warframe] |
        tuple[NotImplementedType] |
        Warframe |
        NotImplementedType) -> None:
    '''Deletes dataclass objects' rows from user lookup tables.

    Args:
        data_objects: Dataclass objects representing rows to delete.
    '''
    set_ids(data_objects)
    data_objects = create_singleton(data_objects)
    data_type = get_type(data_objects)
    with sqlite3.connect(DATABASE) as db:
        match data_type:
            case classes.Warframe:
                sql = Path(DELETE / 'warframes_from_users.sql').read_text()
                params = tuple(
                    {WARFRAME_ID: _.id} for _ in data_objects
                )
            case types.NotImplementedType:
                raise NotImplementedError
            case _:
                raise NoMatchError(data_type)
        db.executemany(sql, params)
        db.commit()


def delete_users_of(
        users:
            tuple[User] |
            User,
        table: str) -> None:
    '''Deletes users' rows from matching lookup table.

    Args:
        users: Dataclass objects representing users to delete.
        table: String representing lookup table to delete from.
    '''
    users = create_singleton(users)
    with sqlite3.connect(DATABASE) as db:
        match table:
            case 'warframes':
                sql = Path(DELETE / 'users_of_warframe.sql').read_text()
                params = tuple(
                    {USER_NAME: user.name} for user in users
                )
            case 'weapons':
                raise NotImplementedError
            case _:
                raise NoMatchError(table)
        db.executemany(sql, params)
        db.commit()
