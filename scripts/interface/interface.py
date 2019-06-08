import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import service.data_manipulations as data_manipulation
import numpy as np
import sampleprocessing.somescriptname as data_processing

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Window(metaclass=_Singleton):
    """
    Основной класс, реализующий окно приложения\n
    Является синглтоном
    """

    def __init__(self):
        self.__init_root()
        self.__init_menubar()

        self.__place_root_center()  # это запускается в самом конце

    def __init_root(self):
        self.__root = tk.Tk()
        self.__root.title("Arya")
        self.__root.iconbitmap("../../resources/drawable/cool_icon.ico")

        self.__figure = Figure(figsize=(5, 5), dpi=100)
        self.__axes = self.__figure.add_subplot(111)
        sample = np.random.normal(0, 3, 1000)
        self.__axes.hist(sample, int(sample.size ** 0.5))
        self.__axes.set_title(u"Тестовые данные")

        self.__plot_canvas = FigureCanvasTkAgg(self.__figure, self.__root)
        self.__plot_canvas.get_tk_widget().grid(row=0, column=0, rowspan=3)

        self.__status_label = tk.Label(self.__root,
                                       text=u"Выборка не загружена",
                                       font="Arial 10",
                                       bg="red")
        self.__status_label.grid(row=0, column=1)

        self.__analyze_btn = tk.Button(self.__root,
                                       text=u"Анализ",
                                       font="Arial 10",
                                       state=tk.DISABLED,
                                       command=self.__on_analyze_btn_click)
        self.__analyze_btn.grid(row=1, column=1)

        self.__analyze_result_text = tk.Text(self.__root)
        self.__analyze_result_text.grid(row=2, column=1)

    def __place_root_center(self):
        """
        Располагает root в центре экрана

        :return:
        """
        ws, hs = self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()
        w, h = self.__root.winfo_width(), self.__root.winfo_height()
        print(w, h)  # TODO убери на релизе
        x, y = ws / 2 - w / 2, hs / 2 - h / 2
        self.__root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # self.__root.resizable(False, False)
        # TODO разберись с размерами root

    def __init_menubar(self):
        """
        Инициализация меню-бара и всех пунктов меню
        Вызывать только после инициализации root

        :return:
        """
        self.__menubar = tk.Menu(self.__root)
        self.__root['menu'] = self.__menubar
        self.__root.iconbitmap("../../resources/drawable/cool_icon.ico")

        self.__file_menu = tk.Menu(self.__menubar, tearoff=0)
        self.__file_menu.add_command(label=u"Загрузить из файла", command=self.__load_from_file)
        self.__file_menu.add_command(label=u"Выход", command=self.__root.quit)

        self.__help_menu = tk.Menu(self.__menubar, tearoff=0)
        self.__help_menu.add_command(label=u"Помощь", command=self.__show_help)
        self.__help_menu.add_command(label=u"О программе", command=self.__show_about)

        self.__menubar.add_cascade(label=u"Файл", menu=self.__file_menu)
        self.__menubar.add_cascade(label=u"Помощь", menu=self.__help_menu)

    def __load_from_file(self):
        """
        Запись обработанных результатов в текстовый файл

        :return:
        """
        filename = filedialog.askopenfilename(initialdir='/',
                                              title=u"Загрузка",
                                              filetypes=((u"Текстовый файл", "*.txt"),))
        if filename != '':
            try:
                sample = data_manipulation.dataload(filename)
                self.__sample = data_processing.Sample(sample)
                self.__status_label.config(text=u"Выборка загружена\n"
                                                u"Имя файла: " + filename.split('/')[-1],
                                           bg="yellow")
                self.__analyze_btn.config(state=tk.ACTIVE)
            except ValueError:
                messagebox.showwarning("Ошибка чтения", "Данные в файле не соответствуют формату")

    def __show_help(self):
        """
        Появление модального окна "Помощь"

        :return:
        """
        help_window = tk.Toplevel(self.__root)
        help_window.transient(self.__root)
        help_window.grab_set()
        help_window.focus_set()

        help_window.title(u"Помощь")
        help_window.iconbitmap("../../resources/drawable/cool_icon.ico")
        help_window.resizable(False, False)

        help_label = tk.Label(help_window, text="Здесь будет помощь")
        help_label.grid(row=0, column=0)

        ok_btn = tk.Button(help_window,
                           padx=30,
                           text="OK",
                           font="Arial 11",
                           command=help_window.destroy)
        ok_btn.grid(row=1, column=0)

        help_window.wait_window()  # это запускается в самом конце

    def __show_about(self):
        """
        Появление модального окна "О программе"

        :return:
        """
        about_window = tk.Toplevel(self.__root)
        about_window.transient(self.__root)
        about_window.grab_set()
        about_window.focus_set()

        about_window.title(u"О программе")
        about_window.iconbitmap("../../resources/drawable/cool_icon.ico")
        about_window.resizable(False, False)

        frame = tk.Frame(about_window)
        frame.grid(row=0, column=0)

        img = Image.open("../../resources/drawable/house_stark.jpg")
        new_width, new_height = 100, 100
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel_app_symbol = tk.Label(frame, image=img)
        panel_app_symbol.grid(row=0, column=0, rowspan=2)

        label_program_name = tk.Label(frame,
                                      text="Arya",
                                      font="Arial 24")
        label_program_name.grid(row=0, column=1)
        label_authors = tk.Label(frame,
                                 text=u"Авторы: cher-di, Iftuga, radislav123",
                                 font="Arial 12")
        label_authors.grid(row=1, column=1)

        ok_btn = tk.Button(about_window,
                           padx=30,
                           text="OK",
                           font="Arial 11",
                           command=about_window.destroy)
        ok_btn.grid(row=1, column=0)

        about_window.wait_window()  # это запускается в самом конце

    def __on_analyze_btn_click(self):
        self.__plot_canvas.get_tk_widget().destroy()

        self.__figure = Figure(figsize=(5, 5), dpi=100)
        self.__axes = self.__figure.add_subplot(111)
        (hist, bins) = self.__sample.get_distribution_function()
        self.__axes.hist(self.__sample.get_sample(), bins=bins)
        self.__axes.set_title(u"Функция распределения")

        self.__plot_canvas.get_tk_widget().destroy()
        self.__plot_canvas = FigureCanvasTkAgg(self.__figure, self.__root)
        self.__plot_canvas.get_tk_widget().grid(row=0, column=0, rowspan=3)

    def run(self):
        """
        Запускает оконный интерфейс, после запуска которого прекращается
        выполнение любых команд интерпретатора Python

        :return:
        """
        self.__root.mainloop()

    @staticmethod
    def __test():
        print("Test")
