'''Module to store database interaction'''


import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / 'warframe.db'

db_connect = sqlite3.connect(DATABASE_DIR)
db_cur = db_connect.cursor()


def user_id(user) -> int:
    '''return matched primary key'''
    query = f'''
        SELECT
            user_id
        FROM
            users u
        WHERE
            u.user_name like "{user}"
        '''
    fetch = db_cur.execute(query)
    result = int(fetch.fetchone()[0])
    return result


def warframe_id(warframe) -> int:
    '''return matched primary key'''
    query = f'''
        SELECT
            warframe_id
        FROM
            warframes w
        WHERE
            w.warframe_name like "{warframe}"
        '''
    fetch = db_cur.execute(query)
    result = int(fetch.fetchone()[0])
    return result


def user_warframes_list(user) -> list:
    '''return list of matched primary keys'''
    query = f'''
        SELECT
            w.warframe_id
        FROM
            warframes w
            JOIN warframes_users_connector wuc ON w.warframe_id = wuc.warframe_id
            JOIN users u ON u.user_id = wuc.user_id
        WHERE
            user_name like "{user}"
        '''
    fetch = db_cur.execute(query)
    result = [int(row[0]) for row in fetch.fetchall()]
    return result


def warframe_users_list(warframe) -> list:
    '''return list of matched primary keys'''
    query = f'''
        SELECT
            u.user_id
        FROM
            users u
            JOIN warframes_users_connector wuc ON u.user_id
            JOIN warframes w ON w.warframe_id = wuc.warframe_id
        WHERE
            w.warframe_name like "{warframe}"
        '''
    fetch = db_cur.execute(query)
    result = [int(row[0]) for row in fetch.fetchall()]
    return result


def users_names(user_id_list) -> list:
    '''return list matching provided primary keys'''
    query = f'''
        SELECT
            u.user_name
        FROM
            users u
        WHERE
            u.user_id IN {user_id_list}
        '''
    fetch = db_cur.execute(query)
    result = [str(row[0]) for row in fetch.fetchall()]
    return result


def warframes_names(warframe_id_list) -> list:
    '''return list matching provided primary keys'''
    query = f'''
        SELECT
            w.warframe_name
        FROM
            warframes w
        WHERE
            w.warframe_id IN {warframe_id_list}
        '''
    fetch = db_cur.execute(query)
    result = [str(row[0]) for row in fetch.fetchall()]
    return result


def insert_user(user_name) -> None:
    '''insert row'''


def insert_warframe(warframe_name) -> None:
    '''insert row'''


def insert_user_warframe(user_id, warframe_id) -> None:
    '''insert primary key pair'''


def update_user_warframe(user_id, warframe_id) -> None:
    '''update primary key pair'''
