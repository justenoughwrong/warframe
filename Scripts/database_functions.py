'''TODO add docstring.'''

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATABASE = BASE_DIR / 'warframe.db'
WARFRAME_NAMES = BASE_DIR / 'InitData' / 'warframes.txt'
SQL_DIR = BASE_DIR / 'sql'


def test():
    a = _get_ids('users', 'joojoo')
    b = _get_ids('warframes', 'voruna, mesa, mag')

    a_str = ','.join(str(e) for e in a)
    b_str = ','.join(str(e) for e in b)
    return _param_dicts(a_str, b_str)


def _split_for_sql(text: str) -> tuple:
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


def _iter_to_string():
    pass


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


def get_all(table: str) -> tuple:
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


def get_from_user(user_name: str, table: str) -> tuple:
    '''Queries lookup tables for matching pairs.

    Queries the user lookup table of the provided args.
    Filters results based on the name arg.

    Ars:
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


def get_users_of(table: str, name: str) -> tuple:
    '''Queries lookup tables for matching pairs.

    Queries the user lookup table of the provided args.
    Filters results based on the name arg.

    Ars:
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


def add(table: str, names: str) -> None:
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
        params = _split_for_sql(names)
        db.executemany(sql, params)
        db.commit()


def add_to(table1: str, name1: str, table2: str, name2: str) -> None:
    '''Inserts rows to corresponding lookup table.

    Args:
        table1: string representing table of name1. Used to determine lookup table.
        name1: string representing first name of lookup pair. Must be singular.
        table2: string representing table of name2. Used to determine lookup table.
        name2: string representing second name of lookup pair. May be one or more.
    '''
    with sqlite3.connect(DATABASE) as db:
        tables = (table1, table2)
        match tables:
            case tables if 'users' in tables and 'warframes' in tables:
                sql = Path(SQL_DIR / 'add_warframe_to_user.sql').read_text()

            case _:
                pass
        print('params need to use user/warframe_id')
        # print(params)
        # if type(name1) == str:
        #     params = {}


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
