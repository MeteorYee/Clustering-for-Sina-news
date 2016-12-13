# Clustering-for-Sina-news
Take advantage of K-means algorithm

## Evaluation
* I used the [corpus](http://www.nlpir.org/?action-viewnews-itemid-103) from _**Fundan University**_ to test my codes. The number of testing files is **2595**, and there are **10 classes** to be catogorized. Finally, I got the result below:

<p align="center"><img src="https://github.com/MeteorYee/Clustering-for-Sina-news/blob/master/images/K-means-precision.png" /></p>

* I also uploaded my testing data and results details, if anyone wants, which are in the files: _**test_corpus_Fudan.zip, BTreport-K10**_, respectively. By the way, GB18030, according to my trials, is the most suitable encoding for this data set.

## Introduction
There are 3 parts in my small system, a **web spider** for Sina news, a **vector-calculating** module and **K-means** algorithm. In this README file, I will just try to introduce the implementation about my K-means algorithm thoroughly. You may see the other two parts in the following two README files:<br>
* [README](https://github.com/MeteorYee/Clustering-for-Sina-news/tree/master/mycrawler) for spider
* [README](https://github.com/MeteorYee/Clustering-for-Sina-news/tree/master/feature_extraction) for feature extraction

to be continued...
