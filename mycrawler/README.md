# Crawler for sina news
Based on BFS algorithm

## Introduction
### PageHandler.py
* the source codes

### PageID
* This file **MUST** exist when the crawler starts to run, which is used to generate **an unique ID** for each downloaded file. You may also revise the content in this file. In fact, it is just an Integer object stored by Cpickle.dump(). I set 100,000 the maximum number of page ID in my code (at line: 168, its initial value is 100,000).

### Url lists
* In order to implement BFS algorithm, I used **3 lists** to store website's urls.
  * _**OpenUrls**_ is the current urls list. Every url in this list is going to be downloaded soon.
  * _**ReadyUrls**_ is the new urls list. Urls in this list are extracted from the contents of the urls in openUrls. Namely, readyUrls is the next-time openUrls.
  * _**CloseUrls**_ stores the urls which have been downloaded. The meaning of its existence is to ensure that crawler won't get a web page twice.

### pagelog.txt
* Just a log file, in case you want to see the running details

## Usage
I may use like this:
```python
sph = SinaPageHandler()
sph.GenerateHomeUrls('http://www.sina.com.cn/')

for i in xrange(10):
  try:
    if i == 0:
      sph.ReadnPage(2000)
    else:
      sph.GoOnReadnPage(200)

  except Exception as e:
    sph.StorePageID()
    sph.StoreOpenUrls()
    sph.StoreReadyUrls()
    sph.StoreCloseUrls()
    print e
```
* _GenerateHomeUrls(url)_<br>
To get the first web page, after that, a new openUrls will be generated.
* _ReadnPage(n)_<br>
Tell the crawler to get n pages.
* _GoOnReadnPage(n)_<br>
The network conditions can be varied, and the method ReadnPage(n) will not always get the number of pages you want, because, for example, we meet a **TIMEOUT**. Hence, this method will make crawler recover and go on to read n pages. All its need is that there **must** be **the three urls lists** in current path.
* _Others_<br>
the rest of methods are used for loading and storing, or some private methods.
