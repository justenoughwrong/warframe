'''Script for GUI class object.'''

import tkinter as tk
from functools import partial
from tkinter import Canvas, ttk

from db_interact import DatabaseHandler

########
# MAIN #
########


class App(tk.Tk):
    '''Main window.'''

    def __init__(self, title: str, size: tuple) -> None:
        '''Create GUI window and frames.'''
        super().__init__()

        # main setup
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        self.database_handler = DatabaseHandler()

        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill='both', expand=True)

        canvas = Canvas(canvas_frame)
        canvas.pack(side='left', fill='both', expand=True)

        scrollbar_ = ttk.Scrollbar(
            canvas_frame, orient='vertical', command=canvas.yview,
        )
        scrollbar_.pack(side='right', fill='y')

        scroll_frame = ttk.Frame(canvas)
        scroll_frame.bind(
            '<Configure>',
            lambda _: canvas.configure(scrollregion=canvas.bbox('all')),
        )

        canvas.configure(yscrollcommand=scrollbar_.set)
        canvas.create_window((0, 0), window=scroll_frame, anchor='n')

        WarframeFrame(scroll_frame, 0, self.database_handler).pack(
            fill='x', expand=True, anchor='center',
        )
        WarframeFrame(scroll_frame, 1, self.database_handler).pack(
            fill='x', expand=True, anchor='center',
        )
        WarframeFrame(scroll_frame, 2, self.database_handler).pack(
            fill='x', expand=True)
        WarframeFrame(scroll_frame, 3, self.database_handler).pack(
            fill='x', expand=True)
        WarframeFrame(scroll_frame, 4, self.database_handler).pack(
            fill='x', expand=True)
        WarframeFrame(scroll_frame, 5, self.database_handler).pack(
            fill='x', expand=True)
        WarframeFrame(scroll_frame, 6, self.database_handler).pack(
            fill='x', expand=True)
        WarframeFrame(scroll_frame, 7, self.database_handler).pack(
            fill='x', expand=True)

        self.mainloop()


#############
# WARFRAMES #
#############


class WarframeFrame(ttk.Frame):
    '''Frame for warframe lookups.'''

    def __init__(
            self,
            parent: ttk.Frame,
            layout: int,
            database_handler: DatabaseHandler,
    ) -> None:
        '''Create and configure frame based on layout input.'''
        super().__init__(parent)

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

        self.button.configure(command=partial(self._toggle_frame, self.frame))
        self.frame.configure(borderwidth=1, relief='sunken')

        self.button.pack()

        self._set_layout()

    def _toggle_frame(self, frame: ttk.Frame) -> None:
        '''Toggle visibility of input frame.'''
        if self.visible:
            self.visible = False
            frame.pack_forget()
        else:
            self.visible = True
            frame.pack()

    def _line_break(self, it: iter) -> str:
        '''Return line break joined string from iterable input.'''
        return str.join('\n', it)

    # LAYOUTS #

    def _set_layout(self) -> None:
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

    def _get_user_names_layout(self) -> None:
        self.button.configure(text='Users')
        self.output.pack()
        self.output.bind('<Map>', self.display_user_names)

    def _get_warframe_names_layout(self) -> None:
        self.button.configure(text='Warframes')
        self.output.pack()
        self.output.bind('<Map>', self.display_warframe_names)

    def _get_user_warframes_layout(self) -> None:
        self.button.configure(text='Search user for warframes')
        self.entry1.pack()
        self.output.pack()
        self.entry1.bind('<Return>', self.display_user_warframes)

    def _get_warframe_users_layout(self) -> None:
        self.button.configure(text='Search warframe for users')
        self.entry1.pack()
        self.output.pack()
        self.entry1.bind('<Return>', self.display_warframe_users)

    def _insert_user_layout(self) -> None:
        self.button.configure(text='Add user')
        self.entry1.pack()
        self.output.pack()
        self.entry1.bind('<Return>', self.insert_user)

    def _insert_warframe_layout(self) -> None:
        self.button.configure(text='Add warframe')
        self.entry1.pack()
        self.output.pack()
        self.entry1.bind('<Return>', self.insert_warframe)

    def _insert_user_warframe_layout(self) -> None:
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

    def _update_user_warframe_layout(self) -> None:
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

    def display_user_names(self, _: ttk.Frame.event_add) -> str:
        '''Event function that returns usernames.'''
        formatted_names = self._line_break(
            self.database_handler.get_user_names())
        self.output.configure(text=formatted_names)

    def display_warframe_names(self, _: ttk.Frame.event_add) -> str:
        '''Event function that returns warframe names.'''
        formatted_names = self._line_break(
            self.database_handler.get_warframe_names())
        self.output.configure(text=formatted_names)

    def display_user_warframes(self, _: ttk.Frame.event_add) -> str:
        '''Event function that returns warframes of the user.'''
        formatted_names = self._line_break(
            self.database_handler.get_user_warframes_names(self.entry1.get()),
        )
        self.output.configure(text=formatted_names)

    def display_warframe_users(self, _: ttk.Frame.event_add) -> str:
        '''Event function that returns users of the warframe.'''
        formatted_name = self._line_break(
            self.database_handler.get_warframe_users_names(self.entry1.get()),
        )
        self.output.configure(text=formatted_name)

    def insert_user(self, _: ttk.Frame.event_add) -> str:
        '''Event function that returns added username.'''
        self.database_handler.insert_user(self.entry1.get())
        self.output.configure(text=f'User "{self.entry1.get()}" added.')

    def insert_warframe(self, _: ttk.Frame.event_add) -> str:
        '''Event function that returns added warframe.'''
        self.database_handler.insert_warframe(self.entry1.get().title())
        self.output.configure(
            text=f'Warframe "{self.entry1.get().title()}" added.')

    def insert_user_warframe(self, _: ttk.Frame.event_add) -> str:
        '''Event function that returns added warframe of user.'''
        user = self.entry1.get()
        warframe = self.entry2.get()
        if user == '' or warframe == '':
            self.output.configure(text='One or more fields empty')
        else:
            self.database_handler.insert_user_warframe(user, warframe)
            self.output.configure(text=f'"{warframe}" added to user {user}')

    def update_user_warframe(self, _: ttk.Frame.event_add) -> str:
        '''Event function that returns altered warframe of user.'''
        user = self.entry1.get()
        old_warframe = self.entry2.get()
        new_warframe = self.entry3.get()
        if user == '' or old_warframe == '' or new_warframe == '':
            self.output.configure(text='One or more fields empty')
        else:
            self.database_handler.update_user_warframe(
                user, old_warframe, new_warframe)
            self.output.configure(
                text=f'{user}\'s warframe "{old_warframe}" updated to "{new_warframe}"',
            )


App('Warframe Data App', (500, 500))
