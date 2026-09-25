'''Test script for debugging purposes only.

WILL_ALTER_DATABASE: Signifies a break point in the script prior to any database altering functions.

non_altering_debug & debug: debug break points to enable quick of the final function in the respective section.
'''

from types import NotImplementedType

import database_functions as df
from classes import User, Warframe

joojoo = User('joojoo')
eee = User('eee')
bird = User('bird')
otter = User('otter')
users = (joojoo, eee, bird, otter)
voruna = Warframe('voruna')
ember = Warframe('ember')
warframes = (voruna, ember)

tse = User('tse')
tss = User('tss')
ttt = User('ttt')
ooo = Warframe('ooo')
okk = Warframe('okk')
occ = Warframe('occ')
fake_warframes = (ooo, okk, occ)
future = NotImplementedType()
incomplete = NotImplementedType()
wip = (future, incomplete)

df.iter_check(future)
df.iter_check(wip)

df.get_type(warframes)
df.get_type(joojoo)

df.tuple_names(users)
df.tuple_names(joojoo)

df.set_ids(voruna)
df.set_ids(warframes)

df._split_for_sql(df.tuple_names(users))  # noqa: SLF001

df.get_all('users')
df.get_all('warframes')

df.get_from_user(joojoo, 'warframes')

df.get_users_of(voruna)

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

df.add(fake_warframes)
df.add(tse)

df.add_to_user(tse, fake_warframes)
df.add_to_user(tse, voruna)

# STRING BASED

df.add_str('users', 'test')

bp = 'break'

# df.add_to('users', 'joojoo', 'warframes', 'voruna')

debug = 'End'
