from scipy import stats
from scipy import array
import numpy


class Sample:
	"""
	Container class for storaging sample data and computing characteristics of a sample
	"""

	__sample__: array
	__normal_distribution_size__ = 10**5
	__normal_distribution__: array
	__p__ = 0.05

	def __init__(self, sample):
		self.__sample__ = sample
		self.__normal_distribution__ = stats.norm.rvs(
			loc = self.mean(),
			scale = self.std(),
			size = self.__normal_distribution_size__
		)

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
		temp = stats.ks_2samp(self.__sample__, self.__normal_distribution__)
		response = {"statistic": temp[0]*self.__sample__.shape[0]**0.5, "p-value": temp[1]}
		return response["p-value"] > self.__p__

	def kolmogorov_norm_test_statistics(self):
		"""
		Define sample are normal distributed or not with level 0.05

		:return: statistics and p-value
		"""
		temp = stats.ks_2samp(self.__sample__, self.__normal_distribution__)
		response = u"статистика критерия: " + temp[0].__str__() + "\np-value: " + temp[1].__str__()
		return response

	def get_distribution_function(self):
		"""
		Return distribution function of the sample data

		:return: tuple of 2 numpy arrays (1 - highs, 2 - bins)
		"""
		return numpy.histogram(self.__sample__, bins = "auto")

	def get_cumulative_distribution_function(self):
		"""
		Return cumulative distribution function of the sample data

		:return: tuple of 2 numpy arrays (1 - highs, 2 - bins)
		"""
		response = [
			numpy.sort(self.__sample__),
			numpy.array(range(self.__sample__.shape[0]))/float(self.__sample__.shape[0])
		]
		return tuple(response)

	def get_normal_distribution_function(self):
		"""
		Return distribution function of random normal sample

		:return: tuple of 2 numpy arrays (1 - highs, 2 - bins)
		"""
		response = list(numpy.histogram(self.__normal_distribution__, bins = "auto"))
		response[0] = response[0]/max(response[0])*max(self.get_distribution_function()[0])
		return tuple(response)

	def get_normal_cumulative_distribution_function(self):
		"""
		Return cumulative distribution function of random normal sample

		:return: tuple of 2 numpy arrays (1 - highs, 2 - bins)
		"""
		response = [
				numpy.sort(self.__normal_distribution__),
				numpy.array(range(self.__normal_distribution_size__))/float(self.__normal_distribution_size__)
		]
		return tuple(response)

	def get_sample(self):
		"""
		Return sample data

		:return: numpy array
		"""
		return self.__sample__
