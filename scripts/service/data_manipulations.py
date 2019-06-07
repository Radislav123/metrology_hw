import numpy as np


def funcname(filename: str):
    """
    Функция принимает строку с расположением файла

    :return: numpy переменная
    """
    return np.loadtxt(filename, dtype=np.str).astype(np.float)
