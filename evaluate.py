# encoding=utf-8

# evaluate the clustering result
#
# Synrey Yee
# 12/09/2016

import numpy as np

def FMeansure(P, R, beta = 1):
	F = (beta * beta + 1) * P * R / (beta * beta * P + R)
	return F

if __name__ == '__main__':
	# EucDistance-
	with open('EucDistance-BTreport-K10', 'r') as ipt:
		content = ipt.readlines()

	# total number
	N = len(content)
	# record dictionary, K : V = clz : { CN : its num }
	record = {}
	# { clt : num }
	clusters = {}
	# { clz : num}
	classes = {}
	for line in content:
		clz, clt = line.split()
		clz = clz[0 : clz.index('-')]

		if clusters.has_key(clt):
			clusters[clt] += 1
		else:
			clusters[clt] = 1

		if classes.has_key(clz):
			classes[clz] += 1
		else:
			classes[clz] = 1
		
		if record.has_key(clt):
			cndict = record[clt]
			if cndict.has_key(clz):
				cndict[clz] += 1
			else:
				cndict[clz] = 1

		else:
			record[clt] = {clz : 1}

	print 'Clusters: %s' % (clusters)
	print 'Classes: %s\n' % (classes)

	# an average used to calculate Purity
	AVG = 0.0

	# mutual information
	MI = 0.0
	# clusters' entropy
	Hclt = 0.0
	# classes' entropy
	Hclz = 0.0

	# Rand-Index-calculating
	RI = 0.0
	TP = 0
	TN = 0
	FP = 0
	FN = 0
	TP_FP = 0
	TP_FN = 0
	TP_FP_FN_TN = N * (N - 1)/ 2

	for clt in record:
		clzdict = record[clt]
		clt_num = int(clusters[clt])
		clt_fnum = float(clusters[clt])
		yes = 0
		mi1 = 0.0
		mi2 = 0.0
		for clz in clzdict:
			num = int(clzdict[clz])
			if num > yes:
				yes = num

			'''
			NOTE HERE!
			There is no need to let 'mi1' be divided by N, because the final result we
			want is Normalized Mutual Information: NMI = 2 * MI / (Hclt + Hclz). As is
			known to us all, division uses the longest clock cycle in CPU. Time is money!
			'''
			mi1 = float(num)
			mi2 = np.log2(N * mi1 / (clt_fnum * float(classes[clz])))
			MI += mi1 * mi2

		AVG += float(yes)
		print 'Cluster%s: %s' % (clt, record[clt])

		# no need to be divided by N too
		Hclt += -(clt_fnum * np.log2(clt_fnum / N))

		TP += yes * (yes - 1) / 2
		TP_FP += clt_num * (clt_num - 1) / 2

	for clz in classes:
		clz_num = int(classes[clz])
		clz_fnum = float(classes[clz])
		# Again, no need to be divided by N too
		Hclz += -(clz_fnum * np.log2(clz_fnum / N))

		TP_FN += clz_num * (clz_num - 1) / 2

	FP = TP_FP - TP
	FN = TP_FN - TP
	TN = TP_FP_FN_TN - TP_FP - FN

	RI = float(TP + TN) / float(TP_FP_FN_TN)

	P = float(TP) / float(TP_FP)
	R = float(TP) / float(TP_FN)

	print '\nPurity: %f' % (AVG / N)
	print 'NMI: %f' % (2 * MI / (Hclt + Hclz))
	print 'Rand Index : %f' % (RI)
	print 'F-Measure, beta = 1: %f' % (FMeansure(P, R))
	print 'F-Measure, beta = 3: %f' % (FMeansure(P, R, beta = 3))
