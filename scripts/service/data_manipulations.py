import numpy as np

def funcname(self, filename: str):
    """
    Функция принимает строку с расположением файла

    :return: numpy переменная
    """
    file = np.loadtxt(filename)
    return file