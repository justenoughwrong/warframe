'''Module to store database interaction'''


import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / 'warframe.db'

db_connect = sqlite3.connect(DATABASE_DIR)
db_cur = db_connect.cursor()


def get_user_id(user_name) -> int:
    '''return matched primary key'''
    query = f'''
        SELECT
            u.user_id
        FROM
            users u
        WHERE
            u.user_name like "{user_name}"
        '''
    fetch = db_cur.execute(query)
    result = int(fetch.fetchone()[0])
    return result


def get_warframe_id(warframe_name) -> int:
    '''return matched primary key'''
    query = f'''
        SELECT
            w.warframe_id
        FROM
            warframes w
        WHERE
            w.warframe_name like "{warframe_name}"
        '''
    fetch = db_cur.execute(query)
    result = int(fetch.fetchone()[0])
    return result


def get_user_warframes(user_name) -> tuple:
    '''return list of matched primary keys'''
    query = f'''
        SELECT
            w.warframe_id
        FROM
            warframes w
            JOIN warframes_users_lookup wul ON w.warframe_id = wul.warframe_id
            JOIN users u ON u.user_id = wul.user_id
        WHERE
            user_name like "{user_name}"
        '''
    fetch = db_cur.execute(query)
    result_list = [int(row[0]) for row in fetch.fetchall()]
    result = tuple(result_list)
    return result


def get_warframe_users(warframe_name) -> tuple:
    '''return list of matched primary keys'''
    query = f'''
        SELECT
            u.user_id
        FROM
            users u
            JOIN warframes_users_lookup wul ON u.user_id
            JOIN warframes w ON w.warframe_id = wul.warframe_id
        WHERE
            w.warframe_name like "{warframe_name}"
        '''
    fetch = db_cur.execute(query)
    result_list = [int(row[0]) for row in fetch.fetchall()]
    result = tuple(result_list)
    return result


def get_users_names(user_id_list) -> tuple:
    '''return list matching provided primary keys'''
    user_id_tuple = tuple(user_id_list)
    query = f'''
        SELECT
            u.user_name
        FROM
            users u
        WHERE
            u.user_id IN {user_id_tuple}
        '''
    fetch = db_cur.execute(query)
    result_list = [str(row[0]) for row in fetch.fetchall()]
    result = tuple(result_list)
    return result


def get_warframes_names(warframe_id_list) -> list:
    '''return list matching provided primary keys'''
    warframe_id_tuple = tuple(warframe_id_list)
    query = f'''
        SELECT
            w.warframe_name
        FROM
            warframes w
        WHERE
            w.warframe_id IN {warframe_id_tuple}
        '''
    fetch = db_cur.execute(query)
    result_list = [str(row[0]) for row in fetch.fetchall()]
    result = tuple(result_list)
    return result


def insert_user(user_name) -> None:
    '''insert row'''
    query = f'''
        INSERT INTO
            users (user_name)
        VALUES
            ("{user_name}")
        '''
    db_cur.execute(query)
    db_connect.commit()


def insert_warframe(warframe_name) -> None:
    '''insert row'''
    query = f'''
        INSERT INTO
            warframes (warframe_name)
        VALUES
            ("{warframe_name}")
        '''
    db_cur.execute(query)
    db_connect.commit()


def insert_user_warframe(user_name, warframe_name) -> None:
    '''insert primary key pair'''
    user_id = get_user_id(user_name)
    warframe_id = get_warframe_id(warframe_name)
    query = f'''
        INSERT INTO
            warframes_users_lookup (user_id, warframe_id)
        VALUES
            ({user_id}, {warframe_id})
        '''
    db_cur.execute(query)
    db_connect.commit()


def update_user_warframe(user_name, old_warframe_name, new_warframe_name) -> None:
    '''update primary key pair'''
    query = f'''
        UPDATE
            warframes_users_lookup
        SET (user_id, warframe_id) = (
            (SELECT u.user_id FROM users u WHERE u.user_name LIKE "{user_name}"),
            (SELECT w.warframe_id FROM warframes w WHERE w.warframe_name LIKE "{new_warframe_name}")
        )
        WHERE
            warframes_users_lookup.user_id = (
                SELECT u.user_id FROM users u WHERE u.user_name LIKE "{user_name}"
            )
        AND
            warframes_users_lookup.warframe_id = (
                SELECT w.warframe_id FROM warframes w WHERE w.warframe_name LIKE "{old_warframe_name}"
            )
        '''
    db_cur.execute(query)
    db_connect.commit()
