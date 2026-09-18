'''Test script for debugging purposes only.

WILL_ALTER_DATABASE: Signifies a break point in the script prior to any database altering functions.

non_altering_debug & debug: debug break points to enable quick of the final function in the respective section.
'''

import database_functions as df
from classes import User, Warframe

joojoo = User('joojoo')
eee = User('eee')
bird = User('bird')
otter = User('otter')
names = (joojoo, eee, bird, otter)
voruna = Warframe('voruna')

tse = User('tse')
tss = User('tss')
ttt = User('ttt')
ooo = Warframe('ooo')
okk = Warframe('okk')
occ = Warframe('occ')
warframes= (ooo, okk, occ)

df.get_names(names)
df.get_names(joojoo)

df._split_for_sql(df.get_names(names))  # noqa: SLF001

df.get_all('users')
df.get_all('warframes')

df.get_from_user(joojoo, 'warframes')

df.get_users_of(voruna, 'warframes')

# STRING BASED

df._split_for_sql_str(' test , tester,tested ')  # noqa: SLF001

df._split(' test , tester,tested ')  # noqa: SLF001

df. _param_dicts('user_name', ' test , tester,tested ,4, 6')  # noqa: SLF001

df. _param_dicts('user_id', ' 8 , 1,2 ,4, 6')  # noqa: SLF001

df._get_ids('users', 'joojoo, bird ,otter,eee')  # noqa: SLF001

df._get_ids('warframes', 'voruna, ember ,mesa,mag')  # noqa: SLF001

df.get_all_str('users')

df.get_from_user_str('joojoo', 'warframes')

df.get_users_of_str('warframes', 'voruna')

non_altering_debug = 'End'

WILL_ALTER_DATABASE = 'Continuing script will alter database!'

df.add(warframes, 'warframes')
df.add(tse, 'users')

# STRING BASED

df.add_str('users', 'test')

bp = 'break'

# df.add_to('users', 'joojoo', 'warframes', 'voruna')

debug = 'End'
