import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import service.data_manipulations as data_manip


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
        self.__initroot()
        self.__initmenubar()

        self.__placerootcenter() # это запускается в самом конце

    def __initroot(self):
        self.__root = tk.Tk()
        self.__root.title("Arya")
        self.__root.iconbitmap("../../resources/drawable/cool_icon.ico")

    def __placerootcenter(self):
        """
        Располагает root в центре экрана

        :return:
        """
        ws, hs = self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()
        w, h = self.__root.winfo_width(), self.__root.winfo_height()
        x, y = ws / 2 - w / 2, hs / 2 - h / 2
        self.__root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def __initmenubar(self):
        """
        Инициализация меню-бара и всех пунктов меню
        Вызывать только после инициализации root

        :return:
        """
        self.__menubar = tk.Menu(self.__root)
        self.__root['menu'] = self.__menubar
        self.__root.iconbitmap("../../resources/drawable/cool_icon.ico")

        self.__filemenu = tk.Menu(self.__menubar, tearoff=0)
        self.__filemenu.add_command(label=u"Загрузить из файла", command=self.__loadfromfile)
        self.__filemenu.add_command(label=u"Выход", command=self.__root.quit)

        self.__helpmenu = tk.Menu(self.__menubar, tearoff=0)
        self.__helpmenu.add_command(label=u"Помощь", command=self.__showhelp)
        self.__helpmenu.add_command(label=u"О программе", command=self.__showabout)

        self.__menubar.add_cascade(label=u"Файл", menu=self.__filemenu)
        self.__menubar.add_cascade(label=u"Помощь", menu=self.__helpmenu)

    def __loadfromfile(self):
        """
        Запись обработанных результатов в текстовый файл

        :return:
        """
        filename = filedialog.askopenfilename(initialdir='/',
                                              title=u"Загрузка",
                                              filetypes=((u"Текстовый файл", "*.txt"),))
        if filename != '':
            try:
                print("Загрузка:", data_manip.funcname(filename))  # TODO поменяй на рабочий код
            except Exception:  # TODO потом поменяй на конкретное исключение
                messagebox.showwarning("Ошибка чтения", "Данные в файле не соответствуют формату")

    def __showhelp(self):
        """
        Появление модального окна "Помощь"

        :return:
        """
        helpwindow = tk.Toplevel(self.__root)
        helpwindow.transient(self.__root)
        helpwindow.grab_set()
        helpwindow.focus_set()

        helpwindow.title(u"Помощь")
        helpwindow.iconbitmap("../../resources/drawable/cool_icon.ico")
        helpwindow.resizable(False, False)

        helplabel = tk.Label(helpwindow,
                           text="Здесь будет помощь")
        helplabel.grid(row=0, column=0)

        okbtn = tk.Button(helpwindow,
                          padx=30,
                          text="OK",
                          font="Arial 11",
                          command=helpwindow.destroy)
        okbtn.grid(row=1, column=0)

        helpwindow.wait_window()  # это запускается в самом конце

    def __showabout(self):
        """
        Появление модального окна "О программе"

        :return:
        """
        aboutwindow = tk.Toplevel(self.__root)
        aboutwindow.transient(self.__root)
        aboutwindow.grab_set()
        aboutwindow.focus_set()

        aboutwindow.title(u"О программе")
        aboutwindow.iconbitmap("../../resources/drawable/cool_icon.ico")
        aboutwindow.resizable(False, False)

        frame = tk.Frame(aboutwindow)
        frame.grid(row=0, column=0)

        img = Image.open("../../resources/drawable/house_stark.jpg")
        new_width, new_height = 100, 100
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panelappsymbol = tk.Label(frame, image=img)
        panelappsymbol.grid(row=0, column=0, rowspan=2)

        labelprogramname = tk.Label(frame,
                                    text="Arya",
                                    font="Arial 24")
        labelprogramname.grid(row=0, column=1)
        labelauthors = tk.Label(frame,
                                text=u"Авторы: cher-di, Iftuga, radislav123",
                                font="Arial 12")
        labelauthors.grid(row=1, column=1)

        okbtn = tk.Button(aboutwindow,
                          padx=30,
                          text="OK",
                          font="Arial 11",
                          command=aboutwindow.destroy)
        okbtn.grid(row=1, column=0)

        aboutwindow.wait_window()  # это запускается в самом конце

    def run(self):
        """
        Запускает оконный интерфейс, после запуска которого прекращается
        выполнение любых команд интерпретатора Python

        :return:
        """
        self.__root.mainloop()

    def __test(self):
        print("Test")
