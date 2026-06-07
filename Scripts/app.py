# Script for GUI class object

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from functools import partial
from db_interact import DatabaseHandler


########
# MAIN #
########


class App(tk.Tk):
    '''Main window'''

    def __init__(self, title, size):
        super().__init__()

        # main setup
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        self.database_handler = DatabaseHandler()

        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill=BOTH, expand=True)

        canvas = Canvas(canvas_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar_ = ttk.Scrollbar(
            canvas_frame, orient='vertical', command=canvas.yview)
        scrollbar_.pack(side=RIGHT, fill=Y)

        scroll_frame = ttk.Frame(canvas)
        scroll_frame.bind('<Configure>', lambda event: canvas.configure(
            scrollregion=canvas.bbox('all')))

        canvas.configure(yscrollcommand=scrollbar_.set)
        canvas.create_window((0, 0), window=scroll_frame, anchor='n')

        WarframeFrame(scroll_frame, 0, self.database_handler).pack(
            fill=X, expand=True, anchor='center')
        WarframeFrame(scroll_frame, 1, self.database_handler).pack(
            fill=X, expand=True, anchor='center')
        WarframeFrame(scroll_frame, 2, self.database_handler).pack(
            fill=X, expand=True)
        WarframeFrame(scroll_frame, 3, self.database_handler).pack(
            fill=X, expand=True)
        WarframeFrame(scroll_frame, 4, self.database_handler).pack(
            fill=X, expand=True)
        WarframeFrame(scroll_frame, 5, self.database_handler).pack(
            fill=X, expand=True)
        WarframeFrame(scroll_frame, 6, self.database_handler).pack(
            fill=X, expand=True)
        WarframeFrame(scroll_frame, 7, self.database_handler).pack(
            fill=X, expand=True)

        # self.bind('<KeyPress-Escape>', quit)

        self.mainloop()


#############
# WARFRAMES #
#############


class WarframeFrame(ttk.Frame):
    '''frame for warframe lookups'''

    def __init__(self, parent, layout, database_handler):
        super().__init__(parent)

        print(self.winfo_parent)
        self.database_handler = database_handler
        self.visible = False
        self.layout = layout

        self.button = ttk.Button(self)
        self.frame = ttk.Frame(self)
        self.entry1_label = ttk.Label(self.frame)
        self.entry1 = ttk.Entry(self.frame)
        self.entry2_label = ttk.Label(self.frame)
        self.entry2 = ttk.Entry(self.frame)
        self.entry3_label = ttk.Label(self.frame)
        self.entry3 = ttk.Entry(self.frame)
        self.output = ttk.Label(self.frame, wraplength=200)

        self.button.configure(command=partial(
            self._toggle_frame, self.frame))
        self.frame.configure(borderwidth=1, relief='sunken')

        self.button.pack()

        self._set_layout()

    def _toggle_frame(self, frame) -> None:
        if self.visible:
            self.visible = False
            frame.pack_forget()
        else:
            self.visible = True
            frame.pack()

    def _line_break(self, it: iter) -> str:
        '''
        Input: iterable object
        Output: line break joined string
        '''
        return str.join('\n', it)

    # LAYOUTS #

    def _set_layout(self):
        match self.layout:
            case 0:
                self._get_user_names_layout()
            case 1:
                self._get_warframe_names_layout()
            case 2:
                self._get_user_warframes_layout()
            case 3:
                self._get_warframe_users_layout()
            case 4:
                self._insert_user_layout()
            case 5:
                self._insert_warframe_layout()
            case 6:
                self._insert_user_warframe_layout()
            case 7:
                self._update_user_warframe_layout()
            case _:
                self.button.configure(text='This button is broken')

    def _get_user_names_layout(self):
        self.button.configure(text='Users')
        self.output.pack()
        self.output.bind('<Map>', self.get_user_names)

    def _get_warframe_names_layout(self):
        self.button.configure(text='Warframes')
        self.output.pack()
        self.output.bind('<Map>', self.get_warframe_names)

    def _get_user_warframes_layout(self):
        self.button.configure(text='Search user for warframes')
        self.entry1.pack()
        self.output.pack()
        self.entry1.bind('<Return>', self.get_user_warframes)

    def _get_warframe_users_layout(self):
        self.button.configure(text='Search warframe for users')
        self.entry1.pack()
        self.output.pack()
        self.entry1.bind('<Return>', self.get_warframe_users)

    def _insert_user_layout(self):
        self.button.configure(text='Add user')
        self.entry1.pack()
        self.output.pack()
        self.entry1.bind('<Return>', self.insert_user)

    def _insert_warframe_layout(self):
        self.button.configure(text='Add warframe')
        self.entry1.pack()
        self.output.pack()
        self.entry1.bind('<Return>', self.insert_warframe)

    def _insert_user_warframe_layout(self):
        self.button.configure(text='Add warframe to user')
        self.entry1_label.configure(text='Enter user')
        self.entry1_label.pack()
        self.entry1.pack()
        self.entry2_label.configure(text='Enter warframe')
        self.entry2_label.pack()
        self.entry2.pack()
        self.output.pack()
        self.entry1.bind('<Return>', self.insert_user_warframe)
        self.entry2.bind('<Return>', self.insert_user_warframe)

    def _update_user_warframe_layout(self):
        self.button.configure(text="Alter user's warframe")
        self.entry1_label.configure(text='Enter user')
        self.entry1_label.pack()
        self.entry1.pack()
        self.entry2_label.configure(text='Enter warframe to alter')
        self.entry2_label.pack()
        self.entry2.pack()
        self.entry3_label.configure(text='Enter new warframe')
        self.entry3_label.pack()
        self.entry3.pack()
        self.output.pack()
        self.entry1.bind('<Return>', self.update_user_warframe)
        self.entry2.bind('<Return>', self.update_user_warframe)
        self.entry3.bind('<Return>', self.update_user_warframe)

    # INTERACTIONS #

    def get_user_names(self, event):
        formatted_names = self._line_break(
            self.database_handler.get_user_names())
        self.output.configure(text=formatted_names)

    def get_warframe_names(self, event):
        formatted_names = self._line_break(
            self.database_handler.get_warframe_names())
        self.output.configure(text=formatted_names)

    def get_user_warframes(self, event):
        formatted_names = self._line_break(self.database_handler.get_user_warframes_names(
            self.entry1.get()))
        self.output.configure(text=formatted_names)

    def get_warframe_users(self, event):
        formatted_name = self._line_break(
            self.database_handler.get_warframe_users_names(self.entry1.get()))
        self.output.configure(text=formatted_name)

    def insert_user(self, event):
        self.database_handler.insert_user(self.entry1.get())
        self.output.configure(text=f'User "{self.entry1.get()}" added.')

    def insert_warframe(self, event):
        self.database_handler.insert_warframe(self.entry1.get().title())
        self.output.configure(
            text=f'Warframe "{self.entry1.get().title()}" added.')

    def insert_user_warframe(self, event):
        user = self.entry1.get()
        warframe = self.entry2.get()
        if user == '' or warframe == '':
            self.output.configure(text='One or more fields empty')
        else:
            self.database_handler.insert_user_warframe(
                user, warframe)
            self.output.configure(
                text=f'"{warframe}" added to user {user}')

    def update_user_warframe(self, event):
        user = self.entry1.get()
        old_warframe = self.entry2.get()
        new_warframe = self.entry3.get()
        if user == '' or old_warframe == '' or new_warframe == '':
            self.output.configure(text='One or more fields empty')
        else:
            self.database_handler.update_user_warframe(
                user, old_warframe, new_warframe)
            self.output.configure(
                text=f'{user}\'s warframe "{old_warframe}" updated to "{new_warframe}"')


App('Warframe Data App', (500, 500))
