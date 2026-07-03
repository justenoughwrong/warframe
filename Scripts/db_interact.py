'''Module to store database interaction.'''


import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / 'warframe.db'
WARFRAME_NAMES_DIR = BASE_DIR / 'InitData' / 'warframes.txt'


class DatabaseHandler:
    '''database handler class.'''

    def __init__(self) -> None:
        '''Create database connection and cursor. Create database if not exists.'''
        self._db_connect = sqlite3.connect(DATABASE_DIR)
        self._db_cur = self._db_connect.cursor()
        self._setup()

    def __del__(self) -> None:
        '''Backup closure of cursor and connection.'''
        self._db_cur.close()
        self._db_connect.close()

    # DATABASE CREATION #

    def _setup(self) -> None:
        '''Build tables if they don't exist.'''
        # USER TABLE #
        query = '''
            CREATE TABLE IF NOT EXISTS users (
            user_id integer PRIMARY KEY,
            user_name varchar(24) NOT NULL UNIQUE
            )
            '''
        self._db_cur.execute(query)
        self._db_connect.commit()

        # WARFRAME TABLE #
        query = '''
            CREATE TABLE IF NOT EXISTS warframes (
            warframe_id integer PRIMARY KEY,
            warframe_name varchar(20) NOT NULL UNIQUE
            )
            '''
        self._db_cur.execute(query)
        self._db_connect.commit()

        # WARFRAME USER LOOKUP TABLE #
        query = '''
            CREATE TABLE IF NOT EXISTS warframes_users_lookup (
            user_id integer,
            warframe_id integer,
            PRIMARY KEY (user_id, warframe_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (warframe_id) REFERENCES warframes(warframe_id)
            )
            '''
        self._db_cur.execute(query)
        self._db_connect.commit()

        # POPULATE WARFRAME TABLE #
        with Path.open(WARFRAME_NAMES_DIR, encoding='utf-8') as f:
            # Get existing name records
            query = '''SELECT warframe_name FROM warframes'''
            records = [
                record[0] for record in self._db_cur.execute(query).fetchall()
            ]
            # Store missing names
            missing_warframes = []
            for line in f:
                stripped_line = line.strip()
                if stripped_line not in records:
                    missing_warframes.append(line)
            # Commit missing names to database
            self.insert_warframes(missing_warframes)

            # WARFRAME INTERACTIONS #

    def _get_user_id(self, user_name: str) -> int:
        '''Return primary key.'''
        params = {
            'user_name': user_name,
        }
        query = '''
            SELECT u.user_id
            FROM users u
            WHERE u.user_name like :user_name
            '''
        fetch = self._db_cur.execute(query, params)
        return int(fetch.fetchone()[0])

    def _get_warframe_id(self, warframe_name: str) -> int:
        '''Return primary key.'''
        params = {
            'warframe_name': warframe_name,
        }
        query = '''
            SELECT w.warframe_id
            FROM warframes w
            WHERE w.warframe_name like :warframe_name
            '''
        fetch = self._db_cur.execute(query, params)
        return int(fetch.fetchone()[0])

    def get_user_names(self) -> tuple:
        '''Return tuple of data.'''
        query = '''
            SELECT u.user_name
            FROM users u
            ORDER BY u.user_name
            '''
        fetch = self._db_cur.execute(query)
        return tuple(
            str(row[0]) for row in fetch.fetchall()
        )

    def get_warframe_names(self) -> tuple:
        '''Return tuple of data.'''
        query = '''
            SELECT w.warframe_name
            FROM warframes w
            ORDER BY w.warframe_name
            '''
        fetch = self._db_cur.execute(query)
        return tuple(
            str(row[0]) for row in fetch.fetchall()
        )

    def get_user_warframes_names(self, user_name: str) -> tuple:
        '''Return tuple of data.'''
        params = {
            'user_name': user_name,
        }
        query = '''
            SELECT w.warframe_name
            FROM warframes w
            WHERE w.warframe_id IN (
                SELECT wul.warframe_id
                FROM warframes_users_lookup wul
                JOIN users u ON
                    wul.user_id = u.user_id
                WHERE u.user_name LIKE :user_name
                )
            ORDER BY w.warframe_name
            '''
        fetch = self._db_cur.execute(query, params)
        return tuple(
            str(row[0]) for row in fetch.fetchall()
        )

    def get_warframe_users_names(self, warframe_name: str) -> tuple:
        '''Return tuple of data.'''
        params = {
            'warframe_name': warframe_name,
        }
        query = '''
            SELECT u.user_name
            FROM users u
            WHERE u.user_id IN (
                SELECT wul.user_id
                FROM warframes_users_lookup wul
                JOIN warframes w ON
                    wul.warframe_id = w.warframe_id
                WHERE w.warframe_name LIKE :warframe_name
            )
            ORDER BY u.user_name
            '''
        fetch = self._db_cur.execute(query, params)
        return tuple(
            str(row[0]) for row in fetch.fetchall()
        )

    def insert_user(self, user_name: str) -> None:
        '''Insert row.'''
        params = {
            'user_name': user_name,
        }
        query = '''
            INSERT OR IGNORE INTO users (user_name)
            VALUES (:user_name)
            '''
        self._db_cur.execute(query, params)
        self._db_connect.commit()

    def insert_warframe(self, warframe_name: str) -> None:
        '''Insert row.'''
        params = {
            'warframe_name', warframe_name,
        }
        query = '''
            INSERT OR IGNORE INTO warframes (warframe_name)
            VALUES (:warframe_name)
            '''
        self._db_cur.execute(query, params)
        self._db_connect.commit()

    def insert_warframes(self, names: iter) -> None:
        '''Insert warframes into the database.'''
        names_formatted = [(name.title(),) for name in names]
        query = '''
            INSERT OR IGNORE INTO warframes (warframe_name)
            VALUES (?)
            '''
        self._db_cur.executemany(query, names_formatted)
        self._db_connect.commit()

    def insert_user_warframe(self, user_name: str, warframe_name: str) -> None:
        '''Insert primary key pair.'''
        user_id = self._get_user_id(user_name)
        warframe_id = self._get_warframe_id(warframe_name)
        params = {
            'user_id': user_id,
            'warframe_id': warframe_id,
        }
        query = '''
            INSERT OR IGNORE INTO warframes_users_lookup (
                user_id,
                warframe_id
            )
            VALUES (
                :user_id,
                :warframe_id
            )
            '''
        self._db_cur.execute(query, params)
        self._db_connect.commit()

    def update_user_warframe(
            self,
            user_name: str,
            old_warframe_name: str,
            new_warframe_name: str,
    ) -> None:
        '''Update primary key pair.'''
        params = {
            'user_name': user_name,
            'old_warframe_name': old_warframe_name,
            'new_warframe_name': new_warframe_name,
        }
        query = '''
            UPDATE warframes_users_lookup
            SET (user_id, warframe_id) = (
                (SELECT u.user_id
                FROM users u
                WHERE u.user_name LIKE :user_name),
                (SELECT w.warframe_id
                FROM warframes w
                WHERE w.warframe_name LIKE :new_warframe_name)
            )
            WHERE warframes_users_lookup.user_id = (
                SELECT u.user_id
                FROM users u
                WHERE u.user_name LIKE :user_name
            )
            AND warframes_users_lookup.warframe_id = (
                SELECT w.warframe_id
                FROM warframes w
                WHERE w.warframe_name LIKE :old_warframe_name
            )
            '''
        self._db_cur.execute(query, params)
        self._db_connect.commit()
