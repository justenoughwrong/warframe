# Script for GUI class object

import tkinter as tk
import sqlite3


class App(tk.Tk):
    def __init__(self):

        # main setup
        self.root = tk.Tk()
        self.root.geometry('500x500')

        # Warframe Section
        self.root.title('Warframe Data')

        self.label0 = tk.Label(self.root, text='Warframes Built')
        self.label0.pack(padx=10, pady=10)

        # frame for full lists of built warframes
        self.builtframe = tk.Frame(self.root)
        self.builtframe.columnconfigure(0, weight=1)
        self.builtframe.columnconfigure(1, weight=1)
        self.builtframe.columnconfigure(2, weight=1)
        self.builtframe.columnconfigure(3, weight=1)

        self.builtframelabel = tk.Label(
            self.builtframe, text='List all frames for selected user')
        self.builtframelabel.grid(columnspan=4, row=0)
        self.btn0 = tk.Button(self.builtframe, text='All')
        self.btn0.grid(column=0, row=1, sticky='we', padx=10, pady=10)
        self.btn0.bind('<ButtonRelease>', self.Btn0)
        self.btn1 = tk.Button(self.builtframe, text='Joojoo')
        self.btn1.grid(column=1, row=1, sticky='we', padx=10, pady=10)
        self.btn1.bind('<ButtonRelease>', self.Btn1)
        self.btn2 = tk.Button(self.builtframe, text='Bird')
        self.btn2.grid(column=2, row=1, sticky='we', padx=10, pady=10)
        self.btn2.bind('<ButtonRelease>', self.Btn2)
        self.btn3 = tk.Button(self.builtframe, text='EEE')
        self.btn3.grid(column=3, row=1, sticky='we', padx=10, pady=10)
        self.btn3.bind('<ButtonRelease>', self.Btn3)

        self.builtframe.pack(pady=10, fill='x')

        # frame for user/warframe specific search
        self.bframe = tk.Frame(self.root)
        self.bframe.columnconfigure(0, weight=1)
        self.bframe.columnconfigure(1, weight=1)

        self.bframelabel = tk.Label(
            self.bframe, text='Both fields must be completed for specific user/frame searches')
        self.bframelabel.grid(columnspan=2, row=0)
        self.elabel0 = tk.Label(self.bframe, text='Enter user')
        self.elabel0.grid(column=0, row=1)
        self.entry0 = tk.Entry(self.bframe)
        self.entry0.grid(column=0, row=2, sticky='we', padx=10)
        self.entry0.bind('<KeyRelease>', self.BuiltFrameSearch)
        self.elabel1 = tk.Label(self.bframe, text='Enter warframe')
        self.elabel1.grid(column=1, row=1)
        self.entry1 = tk.Entry(self.bframe)
        self.entry1.grid(column=1, row=2, sticky='we', padx=10)
        self.entry1.bind('<KeyRelease>', self.BuiltFrameSearch)

        self.bframe.pack(pady=10, fill='x')

        # hotkeys

        self.root.mainloop()

    # Button functions
    def Btn0(self, event):
        if event.state == 264:
            db = sqlite3.connect('././warframe.db')
            cur = db.cursor()
            sqlstr = ('''
                SELECT username, warframe FROM Users
                JOIN WarframesBuilt ON Users.id = WarframesBuilt.user_id
                JOIN Warframes ON WarframesBuilt.warframe_id = Warframes.id
                ''')
            for row in cur.execute(sqlstr):
                print(str(row))

    def Btn1(self, event):
        if event.state == 264:
            db = sqlite3.connect('././warframe.db')
            cur = db.cursor()
            sqlstr = ('''
                SELECT username, warframe FROM Users
                JOIN WarframesBuilt ON Users.id = WarframesBuilt.user_id
                JOIN Warframes ON WarframesBuilt.warframe_id = Warframes.id
                WHERE username = "Joojoo"
                ''')
            for row in cur.execute(sqlstr):
                print(str(row))

    def Btn2(self, event):
        if event.state == 264:
            db = sqlite3.connect('././warframe.db')
            cur = db.cursor()
            sqlstr = ('''
                SELECT username, warframe FROM Users
                JOIN WarframesBuilt ON Users.id = WarframesBuilt.user_id
                JOIN Warframes ON WarframesBuilt.warframe_id = Warframes.id
                WHERE username = "Bird"
                ''')
            for row in cur.execute(sqlstr):
                print(str(row))

    def Btn3(self, event):
        if event.state == 264:
            db = sqlite3.connect('././warframe.db')
            cur = db.cursor()
            sqlstr = ('''
                SELECT username, warframe FROM Users
                JOIN WarframesBuilt ON Users.id = WarframesBuilt.user_id
                JOIN Warframes ON WarframesBuilt.warframe_id = Warframes.id
                WHERE username = "EEE"
                ''')
            for row in cur.execute(sqlstr):
                print(str(row))

    # Search function
    def BuiltFrameSearch(self, event):
        if event.state == 8 and event.keysym == 'Return':
            db = sqlite3.connect('././warframe.db')
            cur = db.cursor()
            cur.execute(f'''
                SELECT username, warframe FROM Users
                JOIN WarframesBuilt ON Users.id = WarframesBuilt.user_id
                JOIN Warframes ON WarframesBuilt.warframe_id = Warframes.id
                WHERE username LIKE (?) AND warframe LIKE (?)
                ''', (self.entry0.get(), self.entry1.get()))
            result = cur.fetchone()
            if result is None:
                print('User has not built this warframe')
            else:
                print(', '.join(result))


App()
