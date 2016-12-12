# encoding=utf-8

# K-means algorithm, implemented by ball tree
#
# Synrey Yee
# 12/06/2016

from feature_extraction import FeatureGene as fg
import cPickle
import time
import BallTree
import copy
import random

class BTKmeansCluster:

	# initialization
	def __init__(self, Kvalue, path, node = 10, func = fg.FeatureGene.CosDistance):
		# K-means' K
		self.__KValue = Kvalue
		# the minimum number of nodes in a ball tree's leaf
		self.__node = node
		# the distance-calculating fuction
		self.__func = func

		self.__FG = fg.FeatureGene(path, encoding = 'GB18030')
		try:
			ipt = open('IDF_file', 'r')
		except:
			print 'Has no IDF file!\n'
			self.__FG.GeneInvDocFreq()
			ipt = open('IDF_file', 'r')
			
		self.__IDF = cPickle.load(ipt)
		ipt.close()

		# K : V = id(vector) : file
		self.__Vfiles = {}

		# get all the vectors dict
		self.__vectors = []

		print 'loading vectors...'
		start = time.clock()

		for file in self.__FG.GetFiles():
			v = self.__FG.TFIDF2vec(file, self.__IDF)
			self.__vectors.append(v)
			self.__Vfiles[id(v)] = file

		end = time.clock()
		print 'spent: %fs' % (end - start)

		# K centor vectors
		self.__Kvecs = self.__FG.GetKFilesVec(self.__KValue, self.__IDF)

		# next K vectors' info
		self.__Newvecs = [[]] * self.__KValue
		# category dict, K : V = category number : [ list of vectors ]
		self.__categories = {}

		self.__miss = 0
		self.__total = 0

	# build ball tree
	def __BuildBallTree(self):
		print 'start building ball tree...'
		start = time.clock()

		r = random.randint(0, len(self.__vectors) - 1)
		# generate center randomly
		center = self.__vectors[r]
		# ball tree's root
		self.__BTroot = BallTree.BallTreeNode(center = center, radius = float('inf'))
		BallTree.GetBallTree(self.__vectors, center, self.__BTroot, self.__node, self.__Distance)

		end = time.clock()
		print 'spent: %fs' % (end - start)

	# the distance
	def __Distance(self, vec1, vec2):
		# to see if they are the same vector
		if id(vec1) == id(vec2):
			dist = 0.0
		else:
			dist = self.__func(vec1, vec2)
			dist = 1.0 / dist

		return dist

	'''
	get the nearest center, based on the distance-calculating function
	after that, store its information
	'''
	def __FindNearestCenter(self, myvec):
		distance = float('inf')
		center_num = 0
		i = 0

		for vec in self.__Kvecs:
			dist = self.__Distance(myvec, vec)
			if dist < distance:
				distance = dist
				center_num = i

			i += 1

		# store the info
		if len(self.__Newvecs[center_num]) == 0:
			self.__Newvecs[center_num] = copy.copy(myvec)
		else:
			self.__Newvecs[center_num] += myvec

		return (center_num + 1)

	'''
	It's time to pick off the leaf!
	If CN is zero, all the vectors in this leaf will be determined by each which category it belongs to.
	If not, all the vectors in this leaf will be categorized into one same CN.
	'''
	def __PickOffLeaf(self, leaf, CN = 0):
		self.__total += 1
		for vec in leaf.area:
			if CN == 0:
				self.__miss += 1
				CN = self.__FindNearestCenter(vec)

			if self.__categories.has_key(CN):
				self.__categories[CN].append(vec)
			else:
				self.__categories[CN] = [vec, ]

	''' 
	Make all the vectors in a particular area become category CN, as we know, the area 
	is stored in ball tree. The parameter should be a ball-tree node accordingly.
	'''
	def __Area2CN(self, btnode, CN):
		if btnode.isLeaf:
			self.__PickOffLeaf(btnode, CN)
			return

		self.__Area2CN(btnode.left, CN)
		self.__Area2CN(btnode.right, CN)

	# search in the ball tree
	def __BTsearch(self, btnode):
		# the list for distances of current center away from K clustering center
		Dlist = []
		for cvec in self.__Kvecs:
			Dlist.append(self.__Distance(btnode.center, cvec))

		lst = sorted(Dlist)
		'''
		When this list is sorted (ascending order), the 1st least one and the 2nd least
		one are lst[0], lst[1] respectively. 
		IIIIIIF lst[0] + btnode.radius <= lst[1] - btnode.radius, we can accordingly conculde
		that all the vectors in this btnode belong to the category whose center to btnode.center
		is lst[0]. We can know from Dlist.index(lst[0]) what the category center is.
		'''
		dmin1 = lst[0]
		dmin2 = lst[1]
		# center distance plus radius
		maxDist = dmin1 + btnode.radius
		# center distance minus radius
		minDist = dmin2 - btnode.radius

		if maxDist <= minDist:
			CN = Dlist.index(dmin1) + 1
			self.__Area2CN(btnode, CN)

		else:
			if btnode.isLeaf:
				self.__PickOffLeaf(leaf = btnode, CN = 0)
				return

			self.__BTsearch(btnode.left)
			self.__BTsearch(btnode.right)

	# iteration
	def __Iteration(self, balltree):
		if balltree:
			CN = random.randint(1, len(self.__Kvecs))
			self.__BTsearch(self.__BTroot)

			print 'miss: %d' % self.__miss
			print 'total: %d' % self.__total
			print 'hit rate: %f' % (float(self.__total - self.__miss) / float(self.__total))

			self.__miss = 0
			self.__total = 0

		else:
			for vec in self.__vectors:
				CN = self.__FindNearestCenter(vec)

				if self.__categories.has_key(CN):
					self.__categories[CN].append(vec)
				else:
					self.__categories[CN] = [vec, ]

	# update
	def __Update(self):
		cnt = 0
		CN = 1
		for Nvec in self.__Newvecs:
			total_num = len(self.__categories[CN])
			Nvec /= total_num
			distance = self.__Distance(Nvec, self.__Kvecs[CN - 1])

			if distance == 1.0:
				cnt += 1

			print 'Category ' + str(CN) + ':',
			print 'distance: ' + str(distance) + ',',
			print 'vector number: ' + str(total_num)

			self.__Kvecs[CN - 1] = Nvec
			CN += 1

		return cnt

	# train
	def Train(self, it_num = 5, balltree = False):
		if balltree:
			self.__BuildBallTree()

		for i in xrange(1, it_num + 1):
			print 'Iteration ' + str(i) + ':'

			start = time.clock()

			self.__Iteration(balltree)
			if self.__Update() >= self.__KValue:
				end = time.clock()
				print 'spent: %fs' % (end - start)
				print 'mission completed'
				break

			if i < it_num:
				self.__Newvecs = [[]] * self.__KValue
				self.__categories = {}
			end = time.clock()
			print 'spent: %fs' % (end - start)
			print 'mission completed'

	# report the result
	def Report(self):
		filename = 'BTreport-K' + str(self.__KValue)
		with open(filename, 'w') as opt:
			for CN in self.__categories:
				for vec in self.__categories[CN]:
					file = self.__Vfiles[id(vec)]
					result = file + ': ' + str(CN) + '\n'
					opt.write(result.encode('utf-8'))


if __name__ == '__main__':
	# the news' path
	path = '/home/meteor/data/Fudan/'
	# path = '/home/meteor/data/sinanews/'
	btkc = BTKmeansCluster(Kvalue = 10, path = path, node = 15)
	btkc.Train(it_num = 5, balltree = True)
	# btkc.Report()
