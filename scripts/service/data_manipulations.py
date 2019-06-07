import numpy as np


def dataload(filename: str):
    """
    Функция принимает строку с расположением файла

    :param filename: имя файла
    :return:
    """
    data = np.loadtxt(filename, dtype=np.str)
    for i, value in enumerate(data):
        data[i] = value.replace(',', '.')
    data = data.astype(np.float)
    return data
