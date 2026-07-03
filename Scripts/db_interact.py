'''Module to store database interaction.'''


import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / 'warframe.db'
WARFRAME_NAMES_DIR = BASE_DIR / 'InitData' / 'warframes.txt'
SQL_DIR = BASE_DIR / 'SQL'


class DatabaseHandler:
    '''Database handler class.'''

    def __init__(self) -> None:
        '''Create database connection and cursor. Create database if not exists.'''
        self._db_connect = sqlite3.connect(DATABASE_DIR)
        self._db_cur = self._db_connect.cursor()
        self._setup()

    def __del__(self) -> None:
        '''Backup closure of cursor and connection.'''
        self._db_cur.close()
        self._db_connect.close()

    def _setup(self) -> None:
        '''Build tables if they don't exist.'''
        # USER TABLE #
        query = self._read_sql(SQL_DIR/'create_user_table.sql')
        self._db_cur.execute(query)
        self._db_connect.commit()

        # WARFRAME TABLE #
        query = self._read_sql(SQL_DIR/'create_warframe_table.sql')
        self._db_cur.execute(query)
        self._db_connect.commit()

        # WARFRAME USER LOOKUP TABLE #
        query = self._read_sql(SQL_DIR/'create_user_warframe_lookup.sql')
        self._db_cur.execute(query)
        self._db_connect.commit()

        # POPULATE WARFRAME TABLE #
        with Path.open(WARFRAME_NAMES_DIR, encoding='utf-8') as f:
            # Get existing name records
            query = 'SELECT warframe_name FROM warframes'
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
            self.add_warframes(missing_warframes)

            # WARFRAME INTERACTIONS #

    def _read_sql(self, sql: Path) -> str:
        '''Return SQL file as a string.'''
        return Path(sql).read_text()

    def _get_user_id(self, user_name: str) -> int:
        '''Return primary key.'''
        params = {'user_name': user_name}
        query = self._read_sql(SQL_DIR/'select_user_id_by_name.sql')
        fetch = self._db_cur.execute(query, params)
        return int(fetch.fetchone()[0])

    def _get_warframe_id(self, warframe_name: str) -> int:
        '''Return primary key.'''
        params = {'warframe_name': warframe_name}
        query = self._read_sql(SQL_DIR/'select_warframe_id_by_name.sql')
        fetch = self._db_cur.execute(query, params)
        return int(fetch.fetchone()[0])

    # PUBLIC FUNCTIONS #

    def get_users(self) -> tuple:
        '''Return tuple of data.'''
        query = self._read_sql(SQL_DIR/'select_user_names.sql')
        fetch = self._db_cur.execute(query)
        return tuple(
            str(row[0]) for row in fetch.fetchall()
        )

    def get_warframes(self) -> tuple:
        '''Return tuple of data.'''
        query = self._read_sql(SQL_DIR/'select_warframe_names.sql')
        fetch = self._db_cur.execute(query)
        return tuple(
            str(row[0]) for row in fetch.fetchall()
        )

    def get_warframes_of_user(self, user_name: str) -> tuple:
        '''Return tuple of data.'''
        params = {'user_name': user_name}
        query = self._read_sql(SQL_DIR/'select_warframes_of_user.sql')
        fetch = self._db_cur.execute(query, params)
        return tuple(
            str(row[0]) for row in fetch.fetchall()
        )

    def get_users_of_warframe(self, warframe_name: str) -> tuple:
        '''Return tuple of data.'''
        params = {'warframe_name': warframe_name}
        query = self._read_sql(SQL_DIR/'select_users_of_warframe.sql')
        fetch = self._db_cur.execute(query, params)
        return tuple(
            str(row[0]) for row in fetch.fetchall()
        )

    def add_user(self, user_name: str) -> None:
        '''Insert row.'''
        params = {'user_name': user_name}
        query = self._read_sql(SQL_DIR/'add_user.sql')
        self._db_cur.execute(query, params)
        self._db_connect.commit()

    def add_warframe(self, warframe_name: str) -> None:
        '''Insert row.'''
        params = {'warframe_name', warframe_name}
        query = self._read_sql(SQL_DIR/'add_warframe.sql')
        self._db_cur.execute(query, params)
        self._db_connect.commit()

    def add_warframes(self, names: iter) -> None:
        '''Insert warframes into the database.'''
        names_formatted = [(name.title(),) for name in names]
        query = self._read_sql(SQL_DIR/'add_warframes.sql')
        self._db_cur.executemany(query, names_formatted)
        self._db_connect.commit()

    def add_warframe_to_user(self, user_name: str, warframe_name: str) -> None:
        '''Insert primary key pair.'''
        user_id = self._get_user_id(user_name)
        warframe_id = self._get_warframe_id(warframe_name)
        params = {
            'user_id': user_id,
            'warframe_id': warframe_id,
        }
        query = self._read_sql(SQL_DIR/'add_warframe_to_user.sql')
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
        query = self._read_sql(SQL_DIR/'update_warframe_of_user.sql')
        self._db_cur.execute(query, params)
        self._db_connect.commit()
