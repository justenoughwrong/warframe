# Script to build initial warframes tables

import sqlite3

# iterables for initial data
users = ('Joojoo', 'Bird', 'Otter', 'EEE')
# store warframes
wfh = open('././initdata/warframes.txt')
warframes = [line.strip() for line in wfh]

# create/connect db
db = sqlite3.connect('warframe.db')
cur = db.cursor()

# USERS

# create users table
cur.executescript('''
    DROP TABLE IF EXISTS Users;
    CREATE TABLE Users (
        id INTEGER PRIMARY KEY,
        username TEXT
        )
    ''')
# populate users table
cur.executemany('INSERT OR IGNORE INTO Users VALUES(?,?)', enumerate(users))
db.commit()

# WARFRAMES

# create warframe table
cur.executescript('''
    DROP TABLE IF EXISTS Warframes;
    CREATE TABLE Warframes (
        id INTEGER PRIMARY KEY,
        warframe TEXT
        )
    ''')
# populate warframe table
cur.executemany('INSERT OR IGNORE INTO Warframes VALUES(?,?)',
                enumerate(warframes))

# warframe built table
cur.executescript('''
        DROP TABLE IF EXISTS WarframesBuilt;
        CREATE TABLE WarframesBuilt (
            user_id INTEGER,
            warframe_id INTEGER,
            PRIMARY KEY (user_id, warframe_id)
            )
    ''')

# populate built frames
# function to insert WarframesBuilt list


def storeframes(file, handle, listname, user):
    file = '././initdata/warframes_' + file + '.txt'
    handle = open(file)
    listname = [line.strip() for line in handle]
    handle.close()
    userindex = users.index(user)
    listname = [(userindex, warframes.index(line))
                for line in warframes if line in listname]
    cur.executemany(
        'INSERT OR IGNORE INTO WarframesBuilt VALUES(?,?)', listname)
    db.commit()


# Joojoo
jfh = 0
jframes = []
storeframes('joojoo', jfh, jframes, 'Joojoo')
# Bird
bfh = 0
bframes = []
storeframes('bird', bfh, bframes, 'Bird')
# EEE
efh = 0
eframes = []
storeframes('eee', efh, eframes, 'EEE')


# WEAPONS

# create weapon table


# COMPANIONS

# create companion table


# ARCANES

db.commit()
