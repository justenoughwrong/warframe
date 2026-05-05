'''Module to store database interaction'''


import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / 'warframe.db'


class DatabaseHandler():
    '''database handler class'''

    def __init__(self):
        self._db_connect = sqlite3.connect(DATABASE_DIR)
        self._db_cur = self._db_connect.cursor()

    def __del__(self):
        self._db_cur.close()
        self._db_connect.close()
        print('database connection closed')

    def _get_user_id(self, user_name) -> int:
        '''return primary key'''
        query = f'''
            SELECT
                u.user_id
            FROM
                users u
            WHERE
                u.user_name like "{user_name}"
            '''
        fetch = self._db_cur.execute(query)
        result = int(fetch.fetchone()[0])
        return result

    def _get_warframe_id(self, warframe_name) -> int:
        '''return primary key'''
        query = f'''
            SELECT
                w.warframe_id
            FROM
                warframes w
            WHERE
                w.warframe_name like "{warframe_name}"
            '''
        fetch = self._db_cur.execute(query)
        result = int(fetch.fetchone()[0])
        return result

    def _get_user_warframes_ids(self, user_name) -> tuple:
        '''return tuple of primary keys'''
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
        fetch = self._db_cur.execute(query)
        result_list = [int(row[0]) for row in fetch.fetchall()]
        result = tuple(result_list)
        return result

    def _get_warframe_users_ids(self, warframe_name) -> tuple:
        '''return tuple of primary keys'''
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
        fetch = self._db_cur.execute(query)
        result_list = [int(row[0]) for row in fetch.fetchall()]
        result = tuple(result_list)
        return result

    def get_user_warframes_names(self, user_name) -> tuple:
        '''return tuple of data'''
        query = f'''
            SELECT
                w.warframe_name
            FROM
                warframes w
                JOIN warframes_users_lookup wul ON w.warframe_id = wul.warframe_id
                JOIN users u ON u.user_id = wul.user_id
            WHERE
                user_name like "{user_name}"
            '''
        fetch = self._db_cur.execute(query)
        result_list = [str(row[0]) for row in fetch.fetchall()]
        result = tuple(result_list)
        return result

    def get_warframe_users_names(self, warframe_name) -> tuple:
        '''return tuple of data'''
        query = f'''
            SELECT
                u.user_name
            FROM
                users u
                JOIN warframes_users_lookup wul ON u.user_id
                JOIN warframes w ON w.warframe_id = wul.warframe_id
            WHERE
                w.warframe_name like "{warframe_name}"
            '''
        fetch = self._db_cur.execute(query)
        result_list = [str(row[0]) for row in fetch.fetchall()]
        result = tuple(result_list)
        return result

    def get_user_names(self) -> tuple:
        '''return tuple of data'''
        query = '''
            SELECT
                u.user_name
            FROM
                users u
            '''
        fetch = self._db_cur.execute(query)
        result_list = [str(row[0]) for row in fetch.fetchall()]
        result = tuple(result_list)
        return result

    def get_warframe_names(self) -> tuple:
        '''return tuple of data'''
        query = '''
            SELECT
                w.warframe_name
            FROM
                warframes w
            '''
        fetch = self._db_cur.execute(query)
        result_list = [str(row[0]) for row in fetch.fetchall()]
        result = tuple(result_list)
        return result

    def insert_user(self, user_name) -> None:
        '''insert row'''
        query = f'''
            INSERT INTO
                users (user_name)
            VALUES
                ("{user_name}")
            '''
        self._db_cur.execute(query)
        self._db_connect.commit()

    def insert_warframe(self, warframe_name) -> None:
        '''insert row'''
        query = f'''
            INSERT INTO
                warframes (warframe_name)
            VALUES
                ("{warframe_name}")
            '''
        self._db_cur.execute(query)
        self._db_connect.commit()

    def insert_user_warframe(self, user_name, warframe_name) -> None:
        '''insert primary key pair'''
        user_id = self._get_user_id(user_name)
        warframe_id = self._get_warframe_id(warframe_name)
        query = f'''
            INSERT INTO
                warframes_users_lookup (user_id, warframe_id)
            VALUES
                ({user_id}, {warframe_id})
            '''
        self._db_cur.execute(query)
        self._db_connect.commit()

    def update_user_warframe(self, user_name, old_warframe_name, new_warframe_name) -> None:
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
        self._db_cur.execute(query)
        self._db_connect.commit()
