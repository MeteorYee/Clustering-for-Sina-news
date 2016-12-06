# encoding=utf-8

# K-means algorithm
#
# Synrey Yee
# 12/04-05/2016

from feature_extraction import FeatureGene as fg
import cPickle
import time

class KmeansCluster:

	# initialization
	def __init__(self, Kvalue, path):
		# K-means' K
		self.__KValue = Kvalue
		self.__FG = fg.FeatureGene(path)
		try:
			ipt = open('IDF_file', 'r')
		except:
			print 'Has no IDF file!\n'
			self.__FG.GeneInvDocFreq()
			ipt = open('IDF_file', 'r')
			
		self.__IDF = cPickle.load(ipt)
		ipt.close()

		# get all the files, this is a dict: K : V = file : category number
		self.__files = self.__FG.GetDictFiles()

		# K centor vectors
		self.__Kvecs = self.__FG.GetKFilesVec(self.__KValue, self.__IDF)

		# next K vectors' info, stored in a dict: K : V = category number : [vector, files number]
		self.__Newvecs = {}
		
	# get the nearest center, based on the distance-calculating function
	# after that, store its information
	def __FindNearestCenter(self, file, func):
		myvec = self.__FG.TFIDF2vec(file, self.__IDF)
		distance = 0.0
		center_num = 0
		i = 0

		for vec in self.__Kvecs:
			dist = func(myvec, vec)
			if dist > distance:
				distance = dist
				center_num = i

			i += 1

		CN = center_num + 1
		# store the info
		if self.__Newvecs.has_key(CN):
			self.__Newvecs[CN][0] += myvec
			self.__Newvecs[CN][1] += 1
		else:
			self.__Newvecs[CN] = [myvec, 1]

		return CN

	# iteration
	def __Iteration(self, func):
		for file in self.__files:
			CN = self.__FindNearestCenter(file, func)
			self.__files[file] = CN

	# update the data
	def __Update(self, func):
		cnt = 0
		for CN in self.__Newvecs:
			Nvec = self.__Newvecs[CN][0]
			total_num = self.__Newvecs[CN][1]
			Nvec /= total_num
			distance = func(Nvec, self.__Kvecs[CN - 1])

			if distance == 1.0:
				cnt += 1

			print 'Category ' + str(CN) + ':',
			print func.__name__ + ' similarity: ' + str(distance) + ',',
			print 'file number: ' + str(total_num)

			self.__Kvecs[CN - 1] = Nvec

		return cnt

	# train
	def Train(self, it_num, func):
		for i in xrange(1, it_num + 1):
			print 'Iteration ' + str(i) + ':'

			start = time.clock()

			self.__Iteration(func)
			if self.__Update(func) == self.__KValue:
				break

			if i < it_num:
				self.__Newvecs = {}
			end = time.clock()
			print 'spent: %fs' % (end - start)

		print 'mission finished'
	# report the result
	def Report(self):
		filename = 'report-K' + str(self.__KValue)
		with open(filename, 'w') as opt:
			for file in self.__files:
				result = file + ': ' + str(self.__files[file]) + '\n'
				opt.write(result.encode('utf-8'))

	# evaluate the result
	def Evaluate(self, func):
		rlist = [0] * self.__KValue
		nlist = [0] * self.__KValue

		for file in self.__files:
			icn = self.__files[file] - 1
			if icn == -1:
				print 'Evaluation failed, files have not been trained!'
				return

			myvec = self.__FG.TFIDF2vec(file, self.__IDF)
			vec = self.__Kvecs[icn]
			rlist[icn] += func(myvec, vec)

		# get the number of each category of files
		for i in xrange(0, self.__KValue):
			nlist[i] = self.__Newvecs[i + 1][1]

		filename = 'evaluation-K' + str(self.__KValue)
		meanDist = 0.0
		with open(filename, 'w') as opt:
			for i in xrange(0, self.__KValue):
				dist = rlist[i]
				num = nlist[i]
				result = 'C ' + str(i + 1) + ': total distance = ' + str(dist) + ', file number = ' + str(num) + '\n'
				opt.write(result.encode('utf-8'))
				meanDist += dist / num

			meanDist /= self.__KValue
			opt.write(('Mean Distance = ' + str(meanDist) + '\n').encode('utf-8'))

		return meanDist


if __name__ == '__main__':
	# the news' path
	path = '/home/meteor/data/sinanews/'
	kc = KmeansCluster(10, path)
	# print kc.FindNearestCenter('2016-11-28-100002', fg.FeatureGene.CosDistance)
	func = fg.FeatureGene.CosDistance
	kc.Train(20, func)
	kc.Report()
	kc.Evaluate(func)
