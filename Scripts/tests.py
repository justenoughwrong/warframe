'''Test script for debugging purposes only.

WILL_ALTER_DATABASE: Signifies a break point in the script prior to any database altering functions.

non_altering_debug & debug: debug break points to enable quick of the final function in the respective section.
'''

from types import NotImplementedType

import database_interface as df
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
fake_users = (tse, tss, ttt)
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

df._tuple_to_singletons(df.tuple_names(users))  # noqa: SLF001

df.get_all('users')
df.get_all('warframes')

df.get_from_user(joojoo, 'warframes')

df.get_users_of(voruna)

non_altering_debug = 'End'

WILL_ALTER_DATABASE = 'Continuing script will alter database!'

# df.add(fake_warframes)
# df.add(tse)

# user none = typeerror
# df.add_to_user(joojoo, ooo)
# df.add_to_user(tse, voruna)

# df.add(fake_users)
# df.delete(fake_users)

# df.add(fake_warframes)
# df.add_to_user(joojoo, fake_warframes)
# df.add_to_user(eee, fake_warframes)
# df.delete_from_users(ooo)
# df.delete_from_users(fake_warframes)

# df.add(fake_users)
# df.add_to_user(tse, warframes)
# df.add_to_user(ttt, warframes)
# df.delete_users_of(fake_users, 'warframes')

bp = 'break'

debug = 'End'
