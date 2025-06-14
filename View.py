from tkinter import Tk, messagebox, Entry, Text, Button, Toplevel, Frame, Label, Scrollbar, Canvas


class WindowNoteView(Toplevel):
    def __init__(self, controller, note=None):
        super().__init__(controller.window_menu)
        self._size_w = 400
        self._size_h = 400
        self._title_page_note = "Note"
        self.controller = controller
        self.title(self._title_page_note)
        self.location_point_user()
        self.protocol("WM_DELETE_WINDOW", controller.on_closing_window_note)
        self.resizable(width=False, height=False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._entry_title = Entry(master=self, bd=3, validate='key',
                                  validatecommand=(self.register(self.controller.validate_input), "%P"))
        self._entry_title.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.set_title_entry(self._entry_title, "Title")
        self._field_text = Text(master=self, bd=3)
        self._field_text.grid(row=1, column=0, sticky="sewn", padx=10, pady=10)
        self._button_add = Button(master=self, text="Ok", command=lambda: self.controller.add_text(note))
        self._button_add.grid(row=2, column=0, sticky="e")
        self._button_delete_note = Button(master=self, text="Del",
                                          command=lambda: self.controller.delete_text_view(note))
        self._button_delete_note.grid(row=2, column=0, sticky="w")

    def main(self):
        self.mainloop()

    def location_point_user(self):
        # Получаем размеры экрана
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Вычисляем координаты для центрирования окна
        x_coordinate = int((screen_width // 3) - (self._size_w // 2))
        y_coordinate = int((screen_height // 3) - (self._size_h // 2))

        self.geometry(f"{self._size_w}x{self._size_h}+{x_coordinate}+{y_coordinate}")

    @property
    def field_text(self):
        return self._field_text.get("1.0", "end").strip()

    @field_text.setter
    def field_text(self, text):
        self._field_text.delete("1.0", "end")
        self._field_text.insert("1.0", text)

    @property
    def entry_title(self):
        return self._entry_title.get()

    @entry_title.setter
    def entry_title(self, value):
        self._entry_title.delete(0, "end")
        self._entry_title.insert(0, value)

    @staticmethod
    def set_title_entry(entry, title):
        entry.delete(0, "end")
        entry.insert(0, title)

    @staticmethod
    def get_exit_window():
        return messagebox.askokcancel("Выход", "Вы действительно хотите выйти?")


class WindowMenuNoteView(Tk):
    def __init__(self, controller):
        super().__init__()
        self._title_menu_note = "Menu"
        self._size_w = 400
        self._size_h = 400
        self.controller = controller
        self.title(self._title_menu_note)
        self.location_point_user()
        self.protocol("WM_DELETE_WINDOW", self.controller.on_closing_window_menu)
        self.resizable(width=False, height=False)
        self.button = Button(master=self, text="Create new", command=self.controller.open_note_window)
        self.button.pack(side="top", anchor="w")
        self.main_frame = Frame(master=self)
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = Canvas(master=self.main_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = Scrollbar(master=self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.scrollbar_frame = Frame(master=self.canvas)
        self.scrollbar_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollbar_frame, anchor="nw")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        for i in range(3):
            self.scrollbar_frame.grid_columnconfigure(i, minsize=(self._size_w - 10) // 3)

    def _on_mousewheel(self, event):
        first, last = self.canvas.yview()
        if first > 0 or last < 1:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def main(self):
        self.mainloop()

    def location_point_user(self):
        # Получаем размеры экрана
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Вычисляем координаты
        x_coordinate = int((screen_width // 3) - (self._size_w // 2))
        y_coordinate = int((screen_height // 3) - (self._size_h // 2))

        self.geometry(f"{self._size_w}x{self._size_h}+{x_coordinate}+{y_coordinate}")

    @staticmethod
    def chang_grid(frame, index):
        frame.grid(row=index // 3 + 1, column=index % 3, sticky="nsew", padx=3, pady=3)

    def add_frame(self, title, text, index):
        frame, button, label_title, label_text = self.create_frame(title, text, self.controller.max_len_text,
                                                                   self.scrollbar_frame)
        frame.grid(row=index // 3 + 1, column=index % 3, sticky="nsew", padx=3, pady=3)
        return frame, button, label_title, label_text

    @staticmethod
    def create_frame(title, text, max_len_text, scrollbar_frame):
        frame = Frame(master=scrollbar_frame, borderwidth=1, bd=1, relief="sunken")
        label_title = Label(frame, text=title)
        label_title.pack(anchor="nw")
        label_text = Label(frame, text=text[:max_len_text])
        label_text.pack(anchor="nw")
        button = Button(frame, text="Open")
        button.pack(side="right", padx=10, pady=5)
        return frame, button, label_title, label_text

    @staticmethod
    def get_exit_window():
        return messagebox.askokcancel("Выход", "Вы действительно хотите выйти?")


class DataFrame:
    def __init__(self):
        self._frame = None
        self._button = None
        self._label_title = None
        self._label_text = None

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

    @property
    def button(self):
        return self._button

    @button.setter
    def button(self, value):
        self._button = value

    @property
    def label_title(self):
        return self._label_title

    @label_title.setter
    def label_title(self, value):
        self._label_title = value

    @property
    def label_text(self):
        return self._label_text

    @label_text.setter
    def label_text(self, value):
        self._label_text = value


class DataTextView:
    def __init__(self, data_text):
        self._data_text = data_text
        self._data_frame = DataFrame()
        self._index = 0
        self._id = None

    @property
    def data_text(self):
        return self._data_text

    @property
    def data_frame(self):
        return self._data_frame

    @data_frame.setter
    def data_frame(self, value=None):
        frame, button, label_title, label_text = value
        self._data_frame.frame = frame
        self._data_frame.button = button
        self._data_frame.label_title = label_title
        self._data_frame.label_text = label_text

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
