# Clustering-for-Sina-news
Taking advantage of K-means algorithm

## Evaluation
### Self-Calculating Precision
* I used the [corpus](http://www.nlpir.org/?action-viewnews-itemid-103) from _**Fundan University**_ to test my codes. The number of testing files is **2595**, and there are **10 classes** to be catogorized. Finally, I got the result below:<br>

<p align="center"><img src="https://github.com/MeteorYee/Clustering-for-Sina-news/blob/master/images/K-means-precision.png" /></p>

* I also uploaded my testing data and results details, if anyone wants, which are in the files: _**test_corpus_Fudan.zip, BTreport-K10**_, respectively. By the way, GB18030, according to my trials, is the most suitable encoding for this data set.

### A More Strong Evaluation
The precision above is calculated by myself. Afterwords, I realized that it could not evaluate a clustering effectively. Hence, I found [THIS](http://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-clustering-1.html), which is from the book: _Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, **Introduction to Information Retrieval**, Cambridge University Press. 2008._ The results are below:
* For clustering calculated by **cosine distance**<br>
<p align="center"><img src="https://github.com/MeteorYee/Clustering-for-Sina-news/blob/master/images/Cos-BTK10.png" /></p>
* For clustering calculated by **Euclidean distance**<br>
<p align="center"><img src="https://github.com/MeteorYee/Clustering-for-Sina-news/blob/master/images/Euc-BTK10.png" /></p>

## Introduction
There are 3 parts in my small system, a **web crawler** for Sina news, a **vector-calculating** module and **K-means** algorithm. In this README file, I will just try to introduce the implementation about my K-means algorithm thoroughly. You may see the other two parts in the following two README files:<br>
* [README](https://github.com/MeteorYee/Clustering-for-Sina-news/tree/master/mycrawler) for crawler
* [README](https://github.com/MeteorYee/Clustering-for-Sina-news/tree/master/feature_extraction) for feature extraction

## Implementation
THREE ways: **file-name-based, vector-based, vector-based with ball tree**
### File-Name-Based
Every 'point' is 'space' is a file name. When calculating the distance between two points, files' corresponding vectors should be generated at first. Hence, the iteration may be slow but it will save a lot of memory. For example, 3000 points in an 87827-dimension space will cost only **120MB** memory and use nearly **21s** in each iteration when using this method, whereas vector-based method will cost nearly **860MB** memory and use only **9s**.
### Vector-Based
More memory and less time. The point is vector.
### Vector-Based with ball tree
Reference: http://blog.csdn.net/skyline0623/article/details/8154911<br><br>
Every node in the ball tree is a hyper-sphere, and the minimum number of points in leaf node can be determined by parameter transfering. Unfortunately, this method is not very mature now, and I am _**still working on it**_ because of the two defects below.
* The time of ball tree building is too long. 3000 87827-dimension vectors need 30 more seconds to build, when the minimum number of points in a leaf is 20.
* The hit rate of this ball tree is really low, which means with ball tree is equal to without.

## Usage
### File-Name-Based
class **KmeansCluster**:<br>
* _**init(self, Kvalue, path)**_<br>
KValue: K value of K-means, path: the corpus path
* _**Train(self, it_num, func)**_<br>
it_num: iteration number, func: the distance-calculating function
* _**Report(self):**_<br>
report the result, see file: _report-K10_
* _**Evaluate(self, func)**_<br>
evaluate the result based on the given function, see file: _evaluation-K10_

### Vector-Based (with Ball Tree)
class **BTKmeansCluster**:<br>
* _**init(self, Kvalue, path, node=10, func)**_<br>
KValue: K value of K-means, path: the corpus path, node: the minimum number of points in leaf node, func: the distance-calculating function
* _**Train(self, it_num=5, balltree=False)**_<br>
it_num: iteration number, balltree = True/False: to use ball tree or not
* _**Report(self):**_<br>
report the result, see file: _BTreport-K10_
