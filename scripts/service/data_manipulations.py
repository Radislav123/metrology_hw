import numpy as np
import sampleprocessing.somescriptname as data_processing


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


def count_curr_results(sample: data_processing.Sample):
    """
    Расчет текущих результатов

    :return: dict с результатами
    """

def save_text_results_to_file(filename: str):
    """
    Запись текстовых результатов в файл

    :return:
    """


def save_plot_results_to_file(filename: str):
    """
    Запись графиков в файл

    :return:
    """
