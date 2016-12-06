# encoding=utf-8

# Feature generator, based on TF-IDF
#
# Synrey Yee
# 11/30/2016

import os
import jieba
import numpy
import cPickle
import time
import random

class FeatureGene:

	# initialization, path is the news path
	def __init__(self, path):
		self.__path = path
		# total number of files
		self.__file_num = 0
		# the file list
		self.__files = None

		for prt, dirs, files in os.walk(self.__path):
			print 'Handling all the files in ' + self.__path + '\n'
			self.__file_num = len(files)
			self.__files = files
			break

	# calculate term frequecy
	def __TermFreq(self, filename):
		with open(self.__path + filename, 'r') as ipt:
			content = ipt.read()

		''' 
		Note here! 
		1. 'cull_all' mode in jieba has already helped us squeeze out the useless symbols,
			such as :, $, %, @, /, ., and the like.
		2. Notice the encoding! My methods like 'utf-8' only
		3. seg_list is a generator.
		'''
		seg_list = jieba.cut(content.decode('utf-8'), cut_all = True)
		# the total words number in this file
		words_num = 0
		# store the result
		dic = {}
		# words we do not need
		stop_words = ['\n', '', ' ', '\t', 'sina', 'http', 'com', 'cn']
		for word in seg_list:
			if word in stop_words:
				continue

			words_num += 1

			if dic.has_key(word):
				dic[word] += 1
			else:
				dic[word] = 1

		return dic, words_num

	# calculate inverse document frequency
	def GeneInvDocFreq(self):
		print 'Generate IDF file\n'
		# include all the words in the raw, K : V = words : [sequence number, IDF]
		Dict = {}
		i = 0
		sqn = 0
		for file in self.__files:
			dic, words_num = self.__TermFreq(file)
			for word in dic:
				if Dict.has_key(word):
					Dict[word][1] += 1
				else:
					Dict[word] = [sqn, 1]
					sqn += 1

			i += 1
			if i % 500 == 0:
				print 'Finish ' + str(i) + ' files.'

		print 'Finally finish ' + str(i) + ' files.'

		for word in Dict:
			tmp = float(self.__file_num) / float(Dict[word][1] + 1)
			Dict[word][1] = numpy.log2(tmp)

		with open('IDF_file', 'w') as opt:
			cPickle.dump(Dict, opt)

		print '\nIDF has been stored into file.'

	# calculate the TF-IDF of the words in a particular file
	# and make it to be vector
	def TFIDF2vec(self, file, IDF):
		TF, words_num = self.__TermFreq(file)
		l = []
		# create vector
		vector = numpy.zeros((len(IDF), ))

		for word in TF:
			if IDF.has_key(word):
				vi, idf = IDF[word]
				tf = numpy.float64(TF[word]) / numpy.float64(words_num)
				tfidf = tf * idf
				vector[vi] = tfidf
			else:
				continue

		return vector

	# calculate the cosine distance between two vectors
	@classmethod
	def CosDistance(clz_obj, vec1, vec2):
		# make vector become 2-dimension matrix
		vec1.shape = (1, vec1.size)
		vec2.shape = (vec2.size, 1)

		# calculate the matrix dot product
		num = numpy.dot(vec1, vec2)[0][0]
		# calculate the matrix's norm
		denom = numpy.linalg.norm(vec1) * numpy.linalg.norm(vec2)
		# cosine
		cos = num / denom

		# normalization
		return (cos * 0.5 + 0.5)

	# calculate the Euclidean distance between two vectors
	@classmethod
	def EucDistance(clz_obj, vec1, vec2):
		edist = numpy.linalg.norm(vec1 - vec2)

		# normalization
		return 1.0 / (edist + 1.0)

	# find all the simiar files according to the given level
	# calculate the distance based on the given function
	def FindSimFiles(self, myfile, level, func):
		myvec = self.TFIDF2vec(myfile, IDF)
		file_list = []
		for file in self.__files:
			if file != myfile:
				vec = self.TFIDF2vec(file, IDF)
				if func(vec, myvec) > level:
					file_list.append(vec)

		return file_list

	# get all the files
	def GetFiles(self):
		return self.__files

	# get all files dict
	def GetDictFiles(self):
		c = [0] * self.__file_num
		dfiles = dict(zip(self.__files, c))
		return dfiles

	# return n file's vectors randomly
	def GetKFilesVec(self, n, IDF):
		ifiles = []
		nvec = []
		top = self.__file_num - 1
		while len(ifiles) < n:
			r = random.randint(0, top)
			if r not in ifiles:
				ifiles.append(r)
				file = self.__files[r]
				nvec.append(self.TFIDF2vec(file, IDF))

		return nvec


if __name__ == '__main__':
	# suit the current OS (windows: \, unix: /)
	# slp = os.sep
	# the files' path
	path = '/home/meteor/data/sinanews/'
	fg = FeatureGene(path)
	try:
		ipt = open('IDF_file', 'r')
	except:
		print 'Has no IDF file!\n'
		fg.GeneInvDocFreq()
		ipt = open('IDF_file', 'r')
			
	IDF = cPickle.load(ipt)
	ipt.close()

	# start = time.clock()
	# vec1 = fg.TFIDF2vec('2016-11-28-100002', IDF)
	# vec2 = fg.TFIDF2vec('2016-11-28-100122', IDF)
	
	'''print FeatureGene.CosDistance(vec1, vec2)
	print FeatureGene.EucDistance(vec1, vec2)
	end = time.clock()
	print 'read: %f' % (end - start)'''

	lst = fg.FindSimFiles('2016-11-28-100002', 0.7, fg.CosDistance)
	for file in lst:
		print file