import tkinter as tk


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

    def run(self):
        """
        Запускает оконный интерфейс, после запуска которого прекращается
        выполнение любых команд интерпретатора Python

        :return:
        """
        self.__root.mainloop()
