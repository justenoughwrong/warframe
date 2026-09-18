'''TODO add docstring.'''

# Built-in Imports
import sqlite3
from pathlib import Path
from types import NotImplementedType

# Custom Imports
from classes import User, Warframe
from exceptions import NoMatchError

# Constants
BASE_DIR = Path(__file__).parent.parent
DATABASE = BASE_DIR / 'warframe.db'
WARFRAME_NAMES = BASE_DIR / 'InitData' / 'warframes.txt'
SQL_DIR = BASE_DIR / 'sql'


def get_names(data_objects: tuple[
    User |
    Warframe |
    NotImplementedType
    ]) -> tuple:
    '''Return a tuple of names from dataclass objects.'''
    try:
        len(data_objects)
        return tuple(
            _.name for _ in data_objects
        )
    except TypeError:
        return (data_objects.name,)


def get_ids(data_objects: tuple[
    User |
    Warframe |
    NotImplementedType
    ]) -> tuple:
    '''Return a tuple of ids from dataclass objects.'''
    try:
        len(data_objects)
        return tuple(
            _.id for _ in data_objects
        )
    except TypeError:
        return (data_objects.id,)


def _split_for_sql(combined_tuple: tuple) -> tuple:
    '''Breaks tuple into individual tuples for each element and returns the new tuple.

    Returns:
        Tuple of tupled values for SQL parameters.
    '''
    return tuple(
        (_,) for _ in combined_tuple
    )


def get_all(table: str) -> tuple:
    '''Retrieves name every row in the matching table. Names are stored in dataclass objects of a corresponding type to the table.

    Args:
        table: String representing the table to fetch from.

    Returns:
        Tuple of dataclass objects containing the corresponding names.
    '''
    with sqlite3.connect(DATABASE) as db:
        match table:
            case 'users':
                query = Path(SQL_DIR / 'select_user_names.sql').read_text()
                result = db.execute(query)
                return tuple(
                    User(str(row[0])) for row in result.fetchall()
                )
            case 'warframes':
                query = Path(SQL_DIR / 'select_warframe_names.sql').read_text()
                result = db.execute(query)
                return tuple(
                    Warframe(str(row[0])) for row in result.fetchall()
                )
            case _:
                raise NoMatchError(table)


def get_from_user(user: User, table: str) -> tuple:
    '''Queries the user lookup table that matches the table arg. Filters results based on the name of the user.

    Args:
        user: Dataclass object that contains the user name. Used to filter the database query.
        table: String representing the table joined by the lookup table.

    Returns:
        Tuple of dataclass objects matching the query results.
    '''
    with sqlite3.connect(DATABASE) as db:
        params = {'user_name': user.name}
        match table:
            case 'warframes':
                query = Path(SQL_DIR / 'select_warframes_of_user.sql').read_text()
                result = db.execute(query, params)
                return tuple(
                    Warframe(str(row[0])) for row in result.fetchall()
                )
            case 'weapons':
                raise NotImplementedError
            case _:
                raise NoMatchError(table)


def get_users_of(data_object: Warframe | NotImplementedType, table: str) -> tuple:
    '''Queries the user lookup table that matches the table arg. Filters results based on the name of the dataclass object.

    Args:
        data_object: Dataclass object that contains the name used to filter the database query.
        table: String representing the table joined by the user lookup.

    Returns:
        Tuple of User objects matching the query results.
    '''
    with sqlite3.connect(DATABASE) as db:
        match table:
            case 'warframes':
                query = Path(SQL_DIR / 'select_users_of_warframe.sql').read_text()
                params = {'warframe_name': data_object.name}
            case 'weapons':
                raise NotImplementedError
            case _:
                raise NoMatchError(table)
        result = db.execute(query, params)
        return tuple(
            User(str(row[0])) for row in result.fetchall()
        )


def add(data_objects: tuple[
            User |
            Warframe |
            NotImplementedType],
            table: str) -> None:
    '''Inserts rows into the table matching the table arg. Saves the changes.

    Args:
        data_objects: Dataclass objects containing the values to insert.
        table: String representing the table to insert to.
    '''
    with sqlite3.connect(DATABASE) as db:
        match table:
            case 'users':
                sql = Path(SQL_DIR / 'add_user.sql').read_text()
            case 'warframes':
                sql = Path(SQL_DIR / 'add_warframe.sql').read_text()
            case 'weapons':
                raise NotImplementedError
            case _:
                raise NoMatchError(table)
        params = _split_for_sql(get_names(data_objects))
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


# def add_to(table1: str, name1: str, table2: str, name2: str) -> None:
#     '''Inserts rows to corresponding lookup table.

#     Args:
#         table1: string representing table of name1. Used to determine lookup table.
#         name1: string representing first name of lookup pair. Must be singular.
#         table2: string representing table of name2. Used to determine lookup table.
#         name2: string representing second name of lookup pair. May be one or more.
#     '''
#     with sqlite3.connect(DATABASE) as db:
#         tables = (table1, table2)
#         match tables:
#             case tables if 'users' in tables and 'warframes' in tables:
#                 sql = Path(SQL_DIR / 'add_warframe_to_user.sql').read_text()

#             case _:
#                 pass
#         print('params need to use user/warframe_id')
#         # print(params)
#         # if type(name1) == str:
#         #     params = {}


# def test():
#     with sqlite3.connect(DATABASE) as db:
#         query = Path(SQL_DIR / 'add_warframe_to_user.sql').read_text()
#         params = (
#             {'user_id': 2, 'warframe_id': 1},
#             {'user_id': 2, 'warframe_id': 2},
#         )
#         db.executemany(query, params)
#         db.commit()


# test()
