# Script for GUI class object

import tkinter as tk
import tkinter.ttk as ttk
import sqlite3

########
# MAIN #
########


class App(tk.Tk):
    def __init__(self, title, size):

        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # widgets
        Warframe(self)

        # Exit Hotkey
        self.bind('<KeyPress-Escape>', quit)

        self.mainloop()

#############
# WARFRAMES #
#############


class Warframe(ttk.Frame):
    '''frame to contain warframe stuff'''

    def __init__(self, parent):
        super().__init__(parent)

        # input warframe to search users who own it
        warframe_entry = ttk.Entry(self)
        warframe_entry.bind('<KeyPress-Return>',
                            lambda event: self.user_list(warframe_entry.get())
                            )
        warframe_entry.pack()

        # table to display users who own warframe
        self.warframe_table = ttk.Treeview(
            self, column='User', show='headings')
        self.warframe_table.pack()

        self.pack()

    def warframe_list(self):
        '''Returns a list of the warframes in warframe.db'''
        sqlstr = 'SELECT warframe FROM Warframes'
        db = sqlite3.connect('././warframe.db')
        cur = db.cursor()
        frames = [str(x[0]) for x in cur.execute(sqlstr)]
        db.close()
        return frames

    def user_list(self, warframe):
        '''Returns list of users of selected warframe'''
        sqlstr = f'''
            SELECT username FROM Users
            JOIN WarframesBuilt ON Users.id = WarframesBuilt.user_id
            JOIN Warframes ON WarframesBuilt.warframe_id = Warframes.id
            WHERE warframe LIKE "{warframe}"
            '''
        db = sqlite3.connect('././warframe.db')
        cur = db.cursor()
        users = [str(x[0]) for x in cur.execute(sqlstr)]
        db.close()

        self.display_users(users)

    def display_users(self, users):
        '''Populates treeview with users'''
        table = self.warframe_table
        for x in table.get_children():
            table.delete(x)
        for user in users:
            table.insert('', tk.END, value=user)


App('Warframe Data App', (500, 500))
