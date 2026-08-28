'''Test script for debugging purposes only.

WILL_ALTER_DATABASE: Signifies a break point in the script
prior to any database altering functions.

non_altering_debug & debug: debug break points to enable quick viewing of the
final function in the respective section.
'''

import database_functions as df

df.test()

df._split_for_sql(' test , tester,tested ')  # noqa: SLF001

df._split(' test , tester,tested ')  # noqa: SLF001

df. _param_dicts('user_name', ' test , tester,tested ,4, 6')  # noqa: SLF001

df. _param_dicts('user_id', ' 8 , 1,2 ,4, 6')  # noqa: SLF001

df._get_ids('users', 'joojoo, bird ,otter,eee')  # noqa: SLF001

df._get_ids('warframes', 'voruna, ember ,mesa,mag')  # noqa: SLF001

df.get_all('users')

df.get_from_user('joojoo', 'warframes')

df.get_users_of('warframes', 'voruna')

non_altering_debug = 'End'

WILL_ALTER_DATABASE = 'Continuing script will alter database!'

df.add('users', 'test')

bp = 'break'

df.add_to('users', 'joojoo', 'warframes', 'voruna')

debug = 'End'
