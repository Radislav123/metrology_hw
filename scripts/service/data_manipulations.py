import numpy as np


def dataload(filename: str):
    """
    Функция принимает строку с расположением файла

    :param filename: имя файла
    :return: возвращает numpy массив
    """
    try:
        data = np.loadtxt(filename, dtype=np.str)
        for i, value in enumerate(data):
            data[i] = value.replace(',', '.')
        data = data.astype(np.float)
    except Exception:
        print("Мб вы пидор?")
        raise ValueError
    return data
