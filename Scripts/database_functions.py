'''TODO add docstring.'''

# Built-in Imports
import sqlite3
import types
from pathlib import Path
from types import NotImplementedType

# Custom Imports
import classes
from classes import User, Warframe
from exceptions import NoMatchError, NotIterableError

# Path Constants
BASE_DIR = Path(__file__).parent.parent
DATABASE = BASE_DIR / 'warframe.db'
WARFRAMES_LIST = BASE_DIR / 'InitData' / 'warframes.txt'
SQL_DIR = BASE_DIR / 'sql'

# Database Column Constants
USER_NAME = 'user_name'
USER_ID = 'user_id'
WARFRAME_NAME = 'warframe_name'
WARFRAME_ID = 'warframe_id'


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
    if iter_check(data_objects):
        return tuple(
            _.name for _ in data_objects
        )
    return (data_objects.name,)


def tuple_ids(
    data_objects:
        tuple[User] |
        tuple[Warframe] |
        tuple[NotImplementedType] |
        User |
        Warframe |
        NotImplementedType) -> tuple:
    '''Return a tuple of ids from dataclass objects.'''
    if iter_check(data_objects):
        return tuple(
            _.id for _ in data_objects
        )
    return (data_objects.id,)


def set_ids(
    data_objects:
        tuple[User] |
        tuple[Warframe] |
        tuple[NotImplementedType] |
        User |
        Warframe |
        NotImplementedType) -> None:
    '''Queries database for ids that match the dataclass object. Tables searched are determined by dataclass object type. Sets id for each dataclass object.'''
    data_type = get_type(data_objects)
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        match data_type:
            case classes.User:
                sql = Path(SQL_DIR / 'select_user_id_by_name.sql').read_text()
                if iter_check(data_objects):
                    for user in data_objects:
                        params = {USER_NAME: user.name}
                        result = db.execute(sql, params).fetchone()
                        user.id = result[USER_ID]
                else:
                    params = {USER_NAME: data_objects.name}
                    result = db.execute(sql, params).fetchone()
                    data_objects.id = result[USER_ID]
            case classes.Warframe:
                sql = Path(SQL_DIR / 'select_warframe_id_by_name.sql').read_text()
                if iter_check(data_objects):
                    for warframe in data_objects:
                        params = {WARFRAME_NAME: warframe.name}
                        result = db.execute(sql, params).fetchone()
                        warframe.id = result[WARFRAME_ID]
                else:
                    params = {WARFRAME_NAME: data_objects.name}
                    result = db.execute(sql, params).fetchone()
                    data_objects.id = result[WARFRAME_ID]
            case types.NotImplementedType:
                raise NotImplementedError
            case _:
                raise NoMatchError(data_type)


def _split_for_sql(combined_tuple: tuple) -> tuple:
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
                query = Path(SQL_DIR / 'select_user_names.sql').read_text()
                results = db.execute(query).fetchall()
                return tuple(
                    User(row[USER_NAME]) for row in results
                )
            case 'warframes':
                query = Path(SQL_DIR / 'select_warframe_names.sql').read_text()
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
                query = Path(SQL_DIR / 'select_warframes_of_user.sql').read_text()
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
                query = Path(SQL_DIR / 'select_users_of_warframe.sql').read_text()
                params = {WARFRAME_NAME: data_object.name}
            case types.NotImplementedType:
                raise NotImplementedError
            case _:
                raise NoMatchError(data_type)
        results = db.execute(query, params).fetchall()
        return tuple(
            User(row[USER_NAME]) for row in results
        )


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
                sql = Path(SQL_DIR / 'add_user.sql').read_text()
            case classes.Warframe:
                sql = Path(SQL_DIR / 'add_warframe.sql').read_text()
            case types.NotImplementedType:
                raise NotImplementedError
            case _:
                raise NoMatchError(data_type)
        params = _split_for_sql(tuple_names(data_objects))
        db.executemany(sql, params)
        db.commit()


def add_to_user(user: User,
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
    data_type = get_type(data_objects)
    with sqlite3.connect(DATABASE) as db:
        match data_type:
            case classes.Warframe:
                sql = Path(SQL_DIR / 'add_warframe_to_user.sql').read_text()
                if iter_check(data_objects):
                    params = tuple(
                        {USER_ID: user.id, WARFRAME_ID: _.id} for _ in data_objects
                    )
                else:
                    params = (
                        {USER_ID: user.id, WARFRAME_ID: data_objects.id},
                    )
            case types.NotImplementedType:
                raise NotImplementedError
            case _:
                raise NoMatchError(data_type)
        db.executemany(sql, params)
        db.commit()


# STRING BASED

def _split_for_sql_str(text: str) -> tuple:
    '''Splits and strips CSV string, then returns as tuples for sql execution.

    Returns:
        tuple of tupled values for SQL parameters.
    '''
    return tuple(
        (e.strip(),) for e in text.split(',')
    )


def _split(text: str) -> tuple:
    '''Splits and strips CSV string, then returns as tuple.'''
    return tuple(
        e.strip() for e in text.split(',')
    )


def _param_dicts(key: str, values: str) -> tuple:
    '''Returns tuple of dictionaries from arguments.

    Args:
        key: string representing key in all dictionaries.
        values: string representing value of each dictionary.

    Returns:
        Tuple of dictionaries with either string or integer values.
        Returns integers if values are int, otherwise returns strings.
    '''
    return tuple(
        {key: int(value)} if value.isdecimal() else {
            key: str(value)}
        for value in _split(values)
    )


def _get_ids(table: str, names: str) -> tuple:
    '''Queries table for ids.

    Retrieves ids from the rows of the matching table and names.
    Splits names via _param_dicts for sql query.

    Args:
        table: string representing the table to fetch from.
        names: string representing names to retrieve ids of.

    Return:
        Tuple of ids as integers
    '''
    with sqlite3.connect(DATABASE) as db:
        match table:
            case 'users':
                query = Path(
                    SQL_DIR / 'select_user_id_by_name.sql').read_text()
                params = _param_dicts('user_name', names)
            case 'warframes':
                query = Path(
                    SQL_DIR / 'select_warframe_id_by_name.sql').read_text()
                params = _param_dicts('warframe_name', names)
            case _:
                print('TODO raised error for table not found.')
        return tuple(
            db.execute(query, param).fetchone()[0] for param in params
        )


def get_all_str(table: str) -> tuple:
    '''Queries table for names.

    Retrieves name from rows in the matching table.

    Args:
        table: string representing the table to fetch from.

    Returns:
        Tuple of names as strings.
    '''
    with sqlite3.connect(DATABASE) as db:
        match table:
            case 'users':
                query = Path(SQL_DIR / 'select_user_names.sql').read_text()
            case 'warframes':
                query = Path(SQL_DIR / 'select_warframe_names.sql').read_text()
            case _:
                print('TODO get_all query failed error')
        result = db.execute(query)
        return tuple(
            str(row[0]) for row in result.fetchall()
        )


def get_from_user_str(user_name: str, table: str) -> tuple:
    '''Queries lookup tables for matching pairs.

    Queries the user lookup table of the provided args.
    Filters results based on the name arg.

    Args:
        user_name: string representing the name to filter the query with.
        table: string representing the table of the lookup.

    Returns:
        Tuple of names as strings.
    '''
    with sqlite3.connect(DATABASE) as db:
        match table:
            case 'warframes':
                query = Path(
                    SQL_DIR / 'select_warframes_of_user.sql').read_text()
            case _:
                print('TODO get_from_users query failed error')
        params = {'user_name': user_name}
        result = db.execute(query, params)
        return tuple(
            str(row[0]) for row in result.fetchall()
        )


def get_users_of_str(table: str, name: str) -> tuple:
    '''Queries lookup tables for matching pairs.

    Queries the user lookup table of the provided args.
    Filters results based on the name arg.

    Args:
        table: string representing the table of the lookup.
        name: string representing the name to filter the query with.

    Returns:
        Tuple of names as strings.
    '''
    with sqlite3.connect(DATABASE) as db:
        match table:
            case 'warframes':
                query = Path(
                    SQL_DIR / 'select_users_of_warframe.sql').read_text()
                params = {'warframe_name': name}
            case _:
                print('TODO get_users_of query failed error')
        result = db.execute(query, params)
        return tuple(
            str(row[0]) for row in result.fetchall()
        )


def add_str(table: str, names: str) -> None:
    '''Inserts rows to corresponding table.

    Matches SQL statement to table.
    Creates tuple to insert values with.
    Saves changes.

    Args:
        table: string representing table to insert to.
        names: string representing name columns of new rows.
    '''
    with sqlite3.connect(DATABASE) as db:
        match table:
            case 'users':
                sql = Path(SQL_DIR / 'add_user.sql').read_text()
            case 'warframes':
                sql = Path(SQL_DIR / 'add_warframe.sql').read_text()
            case _:
                print('TODO add query failed error.')
        params = _split_for_sql_str(names)
        db.executemany(sql, params)
        db.commit()
