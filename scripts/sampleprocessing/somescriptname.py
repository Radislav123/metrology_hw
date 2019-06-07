from scipy import stats
from scipy import array
import numpy


class Sample:
	"""
	Container class for storaging sample data and computing characteristics of sample
	"""

	__sample__: array
	__normal_distribution_size__ = 100000

	def __init__(self, sample):
		self.__sample__ = sample

	def mean(self):
		"""
		Compute mean

		:return: mean value of the sample
		"""
		return self.__sample__.mean()

	def std(self):
		"""
		Compute standard deviation

		:return: standard deviation of the sample
		"""
		return self.__sample__.std()

	def kolmogorov_norm_test(self):
		"""
		Define sample are normal distributed or not with level 0.05

		:return: True if the sample satisfies normal distribution and False if does not
		"""
		temp = stats.kstest(self.__sample__, 'norm')
		response = {"statistic": temp[0], "p-value": temp[1]}
		return response["p-value"] < response["statistic"]

	def get_distribution_function(self):
		"""
		Return distribution function of the sample data

		:return: tuple of 2 numpy arrays
		"""
		return numpy.histogram(self.__sample__, bins = "auto")

	def get_cumulative_distribution_function(self):
		"""
		Return cumulative distribution function of the sample data

		:return: tuple of 2 numpy arrays
		"""
		response: list
		response[0] = numpy.sort(self.__sample__)
		response[1] = numpy.array(range(self.__sample__.shape[0]))/float(self.__sample__.shape[0])
		return tuple(response)

	def get_normal_distribution_function(self):
		"""
		Return distribution function of random normal sample

		:return: tuple of 2 numpy arrays
		"""
		return numpy.histogram(self.__sample__, bins = "auto")

	def get_normal_cumulative_distribution_function(self):
		"""
		Return cumulative distribution function of random normal sample

		:return: tuple of 2 numpy arrays
		"""
		response: list
		response[0] = numpy.sort(numpy.random.normal(size = self.__normal_distribution_size__))
		response[1] = numpy.array(range(self.__normal_distribution_size__))/float(self.__normal_distribution_size__)
		return tuple(response)
