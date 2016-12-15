# Files Preprocessing and Features Extraction

and some necessary methods

## Introduction
* Word Segmentation: **Jieba**
* Feature Extraction: **TF-IDF**
* Distance Calculation: **Euclidean Distance and Cosine Distance**

## Methods
* _**FeatureGene(path, encoding)**_<br>
path: the corpus path, encoding: set the encoding of input content

* _**GeneInvDocFreq()**_<br>
Generate IDF file, used to calculate TF-IDF value

* _**TFIDF2vec(file, IDF)**_<br>
Transforming the content of a file into an vector, based on an IDF file in the current path. If there is no IDF file, method GeneInvDocFreq() should be used in advance.

* _**GetKFilesVec(n, IDF)**_<br>
return n file's vectors randomly

* _**GetFiles(self)**_<br>
return all the files, a list object

* _**GetDictFiles(self)**_<br>
get all the files, a dict object, all values are set by 0

* _**CosDistance(vec1, vec2)**_ class method<br>
calculate the cosine distance between two vectors

* _**EucDistance(clz_obj, vec1, vec2)**_ class method<br>
calculate the Euclidean distance between two vectors

* _**FindSimFiles(self, myfile, level, func)**_<br>
find all the simiar files according to the given level, calculate the distance based on the given function
