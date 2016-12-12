# encoding=utf-8

# ball tree's node
#
# Synrey Yee
# 12/06/2016

import copy

class BallTreeNode:

	# initialization
	def __init__(self, center, radius):
		self.left = None
		self.right = None
		self.isLeaf = False
		self.area = None
		self.center = center
		self.radius = radius


'''
generate the ball tree, where 'area' is a vectors list, 'center' is an vector
'btnode' is a ball-tree node
'''
def GetBallTree(area, center, btnode, node, func):
	if len(area) <= node:
		btnode.area = area
		btnode.isLeaf = True
		return

	# find two new centers
	center1 = FindtheFarthest(me = center, area = area, func = func)
	center2 = FindtheFarthest(me = center1, area = area, func = func)

	# cut off the area into two parts
	area1, r1, area2, r2 = CutArea(area, center1, center2, func)

	btnode.left = BallTreeNode(center1, r1)
	btnode.right = BallTreeNode(center2, r2)

	GetBallTree(area1, center1, btnode.left, node, func)
	GetBallTree(area2, center2, btnode.right, node, func)

# find the farthest point away from 'me' in the 'area', where 'me' is an vector
def FindtheFarthest(me, area, func):
	vector = None
	distance = 0.0

	for vec in area:
		dist = func(me, vec)
		
		if dist > distance:
			distance = dist
			vector = vec

	return vector

# cut off the area into two parts based on the given two centers
def CutArea(area, center1, center2, func):
	area1 = []
	area2 = []
	radius1 = 0.0
	radius2 = 0.0

	for vec in area:
		d1 = func(vec, center1)
		d2 = func(vec, center2)
		if d1 < d2:
			area1.append(vec)
			radius1 = max(d1, radius1)
		else:
			area2.append(vec)
			radius2 = max(d2, radius2)

	return area1, radius1, area2, radius2
