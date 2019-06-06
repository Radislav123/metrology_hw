import tkinter as tk
from tkinter import filedialog


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
        self.__root = tk.Tk()

        self.__initmenubar()

    def __initmenubar(self):
        """
        Инициализация меню-бара и всех пунктов меню
        Вызывать только после инициализации root

        :return:
        """
        self.__menubar = tk.Menu(self.__root)
        self.__root['menu'] = self.__menubar

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
        print("Загрузка:", filename)  # TODO поменяй на рабочий код

    def __showhelp(self):
        """
        Появление модального окна "Помощь"

        :return:
        """
        print(u"Помощь") # TODO поменяй на рабочий код

    def __showabout(self):
        """
        Появление модального окна "О программе"

        :return:
        """
        print(u"О программе") # TODO поменяй на рабочий код

    def run(self):
        """
        Запускает оконный интерфейс, после запуска которого прекращается
        выполнение любых команд интерпретатора Python

        :return:
        """
        self.__root.mainloop()
