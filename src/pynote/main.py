# src/pynote/main.py
from pynote.themes import LIGHT_THEME, DARK_THEME

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "PyNote"


class PyNoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self.title(APP_TITLE)
        self.geometry('800x600')
        self._filepath = None
        self._create_widgets()
        self._create_menu()
        self._bind_shortcuts()
        self._load_theme()

        if self.current_theme == "dark":
            self.apply_theme(DARK_THEME)
        else:
            self.apply_theme(LIGHT_THEME)

    def _create_widgets(self):
        # Text widget with scrollbar
        self.text = tk.Text(self, wrap='word', undo=True)
        self.vsb = ttk.Scrollbar(self, orient='vertical', command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side='right', fill='y')
        self.text.pack(side='left', fill='both', expand=True)

        # status bar
        self.status = tk.StringVar()
        self.status.set('Ln 1, Col 0')
        status_bar = ttk.Label(self, textvariable=self.status, anchor='w')
        status_bar.pack(side='bottom', fill='x')

        # update cursor position
        self.text.bind('<KeyRelease>', self._update_status)
        self.text.bind('<ButtonRelease>', self._update_status)

    def _create_menu(self):
        self.menu = tk.Menu(self)

        filemenu = tk.Menu(self.menu, tearoff=0)
        filemenu.add_command(label='New', command=self.new_file)
        filemenu.add_command(label='Open', command=self.open_file)
        filemenu.add_command(label='Save', command=self.save_file)
        filemenu.add_command(label='Save As', command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label='Toggle Dark Mode', command=self.toggle_theme)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.quit)

        self.menu.add_cascade(label='File', menu=filemenu)
        self.config(menu=self.menu)

    def toggle_theme(self):
        if self.current_theme == "light":
            self.apply_theme(DARK_THEME)
            self.current_theme = "dark"
        else:
            self.apply_theme(LIGHT_THEME)
            self.current_theme = "light"

        self._save_theme()

    def apply_theme(self, theme):
        self.configure(bg=theme["bg"])
        self.text.configure(
            bg=theme["bg"],
            fg=theme["fg"],
            insertbackground=theme["insert_bg"],
            selectbackground=theme["select_bg"],
            selectforeground=theme["select_fg"]
        )

    def _save_theme(self):
        with open("theme.txt", "w") as f:
            f.write(self.current_theme)

    def _load_theme(self):
        try:
            with open("theme.txt", "r") as f:
                self.current_theme = f.read().strip()
        except:
            self.current_theme = "light"



    def _bind_shortcuts(self):
        self.bind('<Control-s>', lambda e: self.save_file())
        self.bind('<Control-o>', lambda e: self.open_file())
        self.bind('<Control-n>', lambda e: self.new_file())
        self.bind('<Control-N>', lambda e: self.new_file())
        self.bind('<Control-z>', lambda e: self.text.event_generate('<<Undo>>'))
        self.bind('<Control-y>', lambda e: self.text.event_generate('<<Redo>>'))

    def new_file(self):
        if self._confirm_discard():
            self.text.delete('1.0', tk.END)
            self._filepath = None
            self.title(APP_TITLE)

    def open_file(self):
        if not self._confirm_discard():
            return
        path = filedialog.askopenfilename(
            filetypes=[('Text Files', '*.txt;*.md;*.py'), ('All Files', '*.*')]
        )
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read()
                self.text.delete('1.0', tk.END)
                self.text.insert('1.0', data)
                self._filepath = path
                self.title(f"{APP_TITLE} - {path}")
            except Exception as e:
                messagebox.showerror('Error', f'Failed to open file: {str(e)}')

    def save_file(self):
        if self._filepath:
            try:
                with open(self._filepath, 'w', encoding='utf-8') as f:
                    f.write(self.text.get('1.0', tk.END))
                self.text.edit_modified(False)
                messagebox.showinfo('Saved', 'File saved successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to save file: {str(e)}')
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Text Files', '*.txt;*.md;*.py'), ('All Files', '*.*')]
        )
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.text.get('1.0', tk.END))
                self._filepath = path
                self.title(f"{APP_TITLE} - {path}")
                self.text.edit_modified(False)
                messagebox.showinfo('Saved', 'File saved successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to save file: {str(e)}')

    def _update_status(self, event=None):
        idx = self.text.index(tk.INSERT).split('.')
        line = idx[0]
        col = idx[1]
        self.status.set(f'Ln {line}, Col {col}')

    def _confirm_discard(self):
        if self.text.edit_modified():
            resp = messagebox.askyesnocancel(
                'Unsaved changes',
                'You have unsaved changes. Save before continuing?'
            )
            if resp is None:
                return False
            if resp:
                self.save_file()
        return True


if __name__ == '__main__':
    app = PyNoteApp()
    app.mainloop()

