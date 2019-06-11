import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import matplotlib
import numpy as np
from PIL import Image, ImageTk

import service.data_manipulations as data_manipulation

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

    __FIG_SIZE = (10, 7)
    __DPI = 100
    __PRECISION = 6

    def __init__(self):
        self.__init_root()
        self.__init_menubar()

        self.__curr_results = None

    def __init_root(self):
        """
        Инициализация главного окна root

        :return:
        """
        self.__root = tk.Tk()
        self.__root.title("Arya")
        self.__root.iconbitmap("../../resources/drawable/cool_icon.ico")

        status_bar = tk.Frame(self.__root)
        status_bar.pack()

        self.__status_label = tk.Label(status_bar,
                                       text=u"Выборка не загружена",
                                       font="Arial 12",
                                       bg="red")
        self.__status_label.grid(row=0, column=0, sticky=tk.E + tk.W + tk.S + tk.N)

        self.__analyze_result_text = tk.Text(status_bar,
                                             font="Arial 12",
                                             width=47,
                                             height=3)
        self.__analyze_result_text.grid(row=0, column=1, sticky=tk.E + tk.W + tk.S + tk.N)
        self.__analyze_result_text.insert('1.0', u"Среднее арифметическое:\n")
        self.__analyze_result_text.insert('2.0', u"СКО:\n")
        self.__analyze_result_text.insert('3.0', u"Критерий Колмогорова:")
        self.__analyze_result_text.config(state=tk.DISABLED)

        figure = Figure(figsize=self.__FIG_SIZE, dpi=self.__DPI)
        axes = figure.add_subplot(111)
        mu, sigma, num = 0, 3, 10 ** 6
        nd = np.random.normal(mu, sigma, num)
        hist, bins = np.histogram(nd, int(num ** 0.5))
        axes.plot(bins, 1 / (sigma * np.sqrt(2 * np.pi)) *
                  np.exp(- (bins - mu) ** 2 / (2 * sigma ** 2)),
                  linewidth=2, color='red')
        axes.set_title(u"Проверка на критерий Колмагорова")

        self.__plot_canvas = FigureCanvasTkAgg(figure, self.__root)
        self.__plot_canvas.get_tk_widget().pack()

        ws, hs = self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()
        w = self.__plot_canvas.get_tk_widget().winfo_reqwidth()
        h = self.__plot_canvas.get_tk_widget().winfo_reqheight() + status_bar.winfo_reqheight()
        x, y = ws / 2 - w / 2, hs / 2 - h / 2
        self.__root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.__root.resizable(False, False)

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
        self.__file_menu.add_command(label=u"Загрузить из файла", command=self.__load_data_from_file)
        self.__file_menu.add_command(label=u"Записать результаты в файлы",
                                     command=self.__save_results_to_file,
                                     state=tk.DISABLED)
        self.__file_menu.add_command(label=u"Выход", command=self.__root.quit)

        self.__help_menu = tk.Menu(self.__menubar, tearoff=0)
        self.__help_menu.add_command(label=u"Помощь", command=self.__show_help)
        self.__help_menu.add_command(label=u"О программе", command=self.__show_about)

        self.__menubar.add_cascade(label=u"Файл", menu=self.__file_menu)
        self.__menubar.add_cascade(label=u"Помощь", menu=self.__help_menu)

    def __load_data_from_file(self):
        """
        Загрузка данных из файла

        :return:
        """
        filename = filedialog.askopenfilename(initialdir='../../data_sample/',
                                              title=u"Загрузка",
                                              filetypes=((u"Текстовый файл (*.txt)", "*.txt"),))
        if filename != '':
            try:
                sample = data_manipulation.data_load(filename)
            except ValueError:
                messagebox.showwarning(u"Ошибка чтения", u"Данные в файле не соответствуют формату")
                return
            else:
                self.__status_label.config(text=u"Выборка загружена\n"
                                                u"Имя файла: " + filename.split('/')[-1],
                                           bg="green")
                self.__curr_results = data_manipulation.count_results(sample)
                self.__plot_new_sample()
                self.__show_characteristics_of_new_sample()

                # возвращаем "Запись результатов в файл" в нормальное состояние
                self.__file_menu.entryconfig(1, state=tk.NORMAL)

    def __save_results_to_file(self):
        """
        Сохранение результатов в файл

        :return:
        """
        curr_output_dir = '../../data_output/'
        filename_text = filedialog.asksaveasfilename(initialdir=curr_output_dir,
                                                     title=u"Сохранение текстовых данных",
                                                     filetypes=((u"Текстовый файл (*.txt)", "*.txt"),))
        if filename_text != '':
            try:
                filename_text = filename_text if filename_text.endswith(".txt") else filename_text + ".txt"
                data_manipulation.save_text_results_to_file(filename_text, self.__curr_results, self.__PRECISION)
            except IOError:
                messagebox.showwarning(u"Ошибка записи", u"Данные харатеристик выборки не были сохранены")
            finally:
                only_filename_text_len = len(filename_text.split('/')[-1])
                curr_output_dir = filename_text[:-only_filename_text_len]

        filename_plot = filedialog.asksaveasfilename(initialdir=curr_output_dir,
                                                     title=u"Сохранение графика",
                                                     filetypes=((u"Portable network graphics (*.png)", "*.png"),))
        if filename_plot != '':
            try:
                filename_plot = filename_plot if filename_plot.endswith(".png") else filename_plot + ".png"
                data_manipulation.save_plot_results_to_file(filename_plot,
                                                            self.__curr_results,
                                                            self.__FIG_SIZE,
                                                            self.__DPI)
            except IOError:
                messagebox.showwarning(u"Ошибка записи", u"Графики не были сохранены")

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

        self.__toplevel_to_center(help_window)

        with open('../../resources/cool_help.txt', 'r') as help_file:
            help_text = help_file.readlines()
        help_text = ''.join(help_text)
        help_label = tk.Label(help_window,
                              text=help_text)
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

        self.__toplevel_to_center(about_window)

        frame = tk.Frame(about_window)
        frame.grid(row=0, column=0)

        img = Image.open("../../resources/drawable/cool_developers.png")
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
                                 text=u"Авторы: cher-di, Iftuga, radislav123\n"
                                      u"meowmik, ещё нет",
                                 font="Arial 12")
        label_authors.grid(row=1, column=1)

        ok_btn = tk.Button(about_window,
                           padx=30,
                           text="OK",
                           font="Arial 11",
                           command=about_window.destroy)
        ok_btn.grid(row=1, column=0)

        about_window.wait_window()  # это запускается в самом конце

    def __plot_new_sample(self):
        """
        Отрисовка графиков с новыми данными

        :return:
        """
        self.__plot_canvas.get_tk_widget().destroy()

        figure = Figure(figsize=self.__FIG_SIZE, dpi=self.__DPI)
        axes1 = figure.add_subplot(211)
        axes2 = figure.add_subplot(212)

        (hist, bins) = self.__curr_results["plot1"]["df"]
        axes1.hist(self.__curr_results["sample"], bins=bins, color="blue", label=u"Функция распределения")
        (hist, bins) = self.__curr_results["plot1"]["ndf"]
        axes1.plot(bins[:-1], hist, color="orange", label=u"Функция нормального распределения")
        axes1.legend()
        axes1.set_title(u"Функция распределения")

        (bins, hist) = self.__curr_results["plot2"]["cdf"]
        axes2.plot(bins, hist, color="blue", label=u"Кумулятивная функция распределения")
        (bins, hist) = self.__curr_results["plot2"]["cndf"]
        axes2.plot(bins, hist, color="green", label=u"Кумулятивная функция нормального распределения")
        axes2.legend()
        axes2.set_title(u"Кумулятивная функция распределения")

        self.__plot_canvas.get_tk_widget().destroy()
        self.__plot_canvas = FigureCanvasTkAgg(figure, self.__root)
        self.__plot_canvas.get_tk_widget().pack()

    def __show_characteristics_of_new_sample(self):
        """
        Вывод характеристик новой выборки
        1. Среднее арифметическое
        2. СКО
        3. Результат проверки критерия Колмогорова
        4. Результат проверки нормального критерия Колмогорова

        :return:
        """
        self.__analyze_result_text.config(state=tk.NORMAL)
        self.__analyze_result_text.delete('1.0', tk.END)

        self.__analyze_result_text.insert('1.0', u"Среднее арифметическое: {}\n".format(
            data_manipulation.to_fixed(self.__curr_results["mean"], self.__PRECISION)))
        self.__analyze_result_text.insert('2.0', u"СКО: {}\n".format(
            data_manipulation.to_fixed(self.__curr_results["std"], self.__PRECISION)))

        kolmogorov_test_result = u"удовлетворяет" if self.__curr_results["test"] else u"не удовлетворяет"
        self.__analyze_result_text.insert('3.0', u"Критерий Колмогорова: {} на уровне 0.05\n".format(kolmogorov_test_result))

        self.__analyze_result_text.config(state=tk.DISABLED)

    def run(self):
        """
        Запускает оконный интерфейс, после запуска которого прекращается
        выполнение любых команд интерпретатора Python

        :return:
        """
        self.__root.mainloop()

    @staticmethod
    def __toplevel_to_center(toplevel):
        """
        Расположение окна по центру

        :return:
        """
        toplevel.update_idletasks()

        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()

        toplevel_width = toplevel.winfo_reqwidth()
        toplevel_height = toplevel.winfo_reqheight()

        x = screen_width / 2 - toplevel_width / 2
        y = screen_height / 2 - toplevel_height / 2

        toplevel.geometry("+%d+%d" % (x, y))
