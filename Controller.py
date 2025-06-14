from Model import DataNote
from View import WindowNoteView, WindowMenuNoteView, DataTextView
import sqlite3


class Controller:
    def __init__(self):
        self.window_menu = WindowMenuNoteView(self)
        self.window_note = None
        self.max_len_text = 12
        self.max_len_title = 12
        self.table_name = "notes"
        self.notes_list = []
        self.db = sqlite3.connect("DataNote.db")
        self.cursor_db = self.db.cursor()
        self.check_tabel()
        self.create_text_view_in_db()

    def main(self):
        self.window_menu.main()

    def check_tabel(self):
        if not self.table_exists(self.table_name):
            self.cursor_db.execute("""
            CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            text_note TEXT NOT NULL
            );
                                   """)
        self.db.commit()

    def open_note_window(self):
        self.window_note = WindowNoteView(self)
        self.window_note.grab_set()

    def open_note_window_2(self, note):
        self.window_note = WindowNoteView(self, note)
        self.window_note.field_text = note.data_text.text
        self.window_note.entry_title = note.data_text.title

    def on_closing_window_note(self):
        if self.window_note.get_exit_window():
            self.window_note_destroy()

    def window_note_destroy(self):
        self.window_note.destroy()
        self.window_note = None

    def create_text_view_in_db(self):
        self.cursor_db.execute('SELECT * FROM notes')
        rows = self.cursor_db.fetchall()
        for row in rows:
            # row = (id, title, text)
            data_note = DataNote()
            data_note.title = row[1]
            data_note.text = row[2]
            note = DataTextView(data_note)
            # У database id начинается с 1
            note.index = len(self.notes_list)
            note.id = row[0]
            self.notes_list.append(note)
            note.data_frame = self.window_menu.add_frame(note.data_text.title[:self.max_len_title],
                                                         note.data_text.text[:self.max_len_text],
                                                         note.index)
            note.data_frame.button.config(command=lambda n=note: self.open_note_window_2(n))

    def on_closing_window_menu(self):
        if self.window_menu.get_exit_window():
            self.window_menu.destroy()
            # self.clear_db()
            if self.notes_list:
                for el in self.notes_list:
                    self.cursor_db.execute("SELECT * FROM notes WHERE id = ?", (el.id,))
                    result = self.cursor_db.fetchone()
                    if not result:
                        self.add_in_db(el)
                    self.db.commit()

            self.db.close()

    def add_in_db(self, el):
        title, text = el.data_text.title, el.data_text.text
        self.cursor_db.execute("""
                               INSERT INTO notes (title, text_note)
                               VALUES (?, ?)
                               """, (title, text))
        self.db.commit()

    def add_text(self, note):
        if not note:
            note = DataTextView(DataNote())
            self.set_title_text(note.data_text)
            note.index = len(self.notes_list)
            self.notes_list.append(note)
            note.data_frame = self.window_menu.add_frame(note.data_text.title[:self.max_len_title],
                                                         note.data_text.text[:self.max_len_text],
                                                         note.index)
            note.data_frame.button.config(command=lambda: self.open_note_window_2(note))
            self.window_note_destroy()

        else:
            title = self.window_note.entry_title
            text = self.window_note.field_text
            id_note = note.id
            self.set_title_text(note.data_text)
            note.data_frame.label_text.config(text=note.data_text.text[:self.max_len_text])
            note.data_frame.label_title.config(text=note.data_text.title[:self.max_len_title])
            self.window_note_destroy()
            self.cursor_db.execute("UPDATE notes SET title=?, text_note=? WHERE id=?", (title, text, id_note))
            self.db.commit()

    def delete_text_view(self, note):
        if note:
            note.data_frame.frame.destroy()
            self.notes_list.pop(note.index)
            self.cursor_db.execute("DELETE FROM notes WHERE id = ?", (note.id,))
            self.db.commit()
            del note
            self.window_note_destroy()
            self.displacement_view_notes()

    def displacement_view_notes(self):
        for i, el in enumerate(self.notes_list):
            el.index = i
            self.window_menu.chang_grid(el.data_frame.frame, i)

    def set_title_text(self, data_note):
        data_note.title = self.window_note.entry_title
        data_note.text = self.window_note.field_text

    def table_exists(self, table_name):
        self.cursor_db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return self.cursor_db.fetchone() is not None

    @staticmethod
    def validate_input(new_value):
        return len(new_value) <= 50

    @staticmethod
    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()
