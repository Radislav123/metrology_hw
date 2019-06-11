import numpy as np
from matplotlib import pyplot as plt

import sampleprocessing.somescriptname as data_processing


def data_load(filename: str):
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


def count_results(sample):
    """
    Расчет текущих результатов
    Макет dict:
    results = {"sample": ,
               "mean": ,
               "std": ,
               "test": ,
               "plot1": {"df": ,
                         "ndf": },
               "plot2": {"cdf": ,
                         "cndf": }}

    :return: dict с результатами
    """
    sample = data_processing.Sample(sample)
    results = {"sample": sample.get_sample(),
               "mean": sample.mean(),
               "std": sample.std(),
               "test": sample.kolmogorov_norm_test(),
               "plot1": {"df": sample.get_distribution_function(),
                         "ndf": sample.get_normal_distribution_function()},
               "plot2": {"cdf": sample.get_cumulative_distribution_function(),
                         "cndf": sample.get_normal_cumulative_distribution_function()}}
    return results


def save_text_results_to_file(filename: str, results: dict, precision: int):
    """
    Запись текстовых результатов в файл
    1. Среднее арифметическое
    2. СКО
    3. Результат проверки критерия Колмогорова

    :param filename: имя файла
    :param results: результаты для записи
    :param precision: количество знаков после запятой для чисел с плавающей запятой
    :return:
    """
    with open(filename, 'w') as output_text_file:
        output_text_file.write(u"Среднее арифметическое: {}\n".
                               format(to_fixed(results["mean"], precision)))
        output_text_file.write(u"СКО: {}\n".
                               format(to_fixed(results["std"], precision)))
        kolmogorov_test_result = u"удовлетворяет" if results["test"] else u"не удовлетворяет"
        output_text_file.write(u"Критерий Колмогорова: {}\n".format(kolmogorov_test_result))


def save_plot_results_to_file(filename: str, results: dict, fig_size: tuple, dpi: int):
    """
    Запись графиков в файл

    :param filename: имя файла
    :param results: результаты для записи
    :param fig_size: размер графика
    :param dpi: разрешение
    :return:
    """
    figure = plt.Figure(figsize=fig_size, dpi=dpi)
    axes1 = figure.add_subplot(211)
    axes2 = figure.add_subplot(212)

    (hist, bins) = results["plot1"]["df"]
    axes1.hist(results["sample"], bins=bins, color="blue", label=u"Функция распределения")
    (hist, bins) = results["plot1"]["ndf"]
    axes1.plot(bins[:-1], hist, color="orange", label=u"Функция нормального распределения")
    axes1.legend()
    axes1.set_title(u"Функция распределения")

    (bins, hist) = results["plot2"]["cdf"]
    axes2.plot(bins, hist, color="blue", label=u"Кумулятивная функция распределения")
    (bins, hist) = results["plot2"]["cndf"]
    axes2.plot(bins, hist, color="green", label=u"Кумулятивная функция нормального распределения")
    axes2.legend()
    axes2.set_title(u"Кумулятивная функция распределения")

    figure.savefig(filename)


def to_fixed(num_obj, digits=0):
    """
    Принимает число с плавающей запятой, и возвращает его,
    с digits знаками после запятой

    :param num_obj: число с плавающей запятой
    :param digits: сколько оставить знаков после запятой
    :return: число с плавающей запятой с digits знаками после запятой
    """
    return f"{num_obj:.{digits}f}"
