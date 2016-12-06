# -*- coding:utf-8 -*-

# Handle the pages of sina
#
# Synrey Yee
# 11/26--27/2016

import requests
from bs4 import BeautifulSoup as btsp
import re
import cPickle
import time
import datetime

class SinaPageHandler:

	# initialization
	def __init__(self):

		# page ID, there must be a file storing the ID in the current path
		self.__PID__ = 100000

		user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
		accept = 'image/webp,image/*,*/*;q=0.8'
		self.__headers = { 'User-Agent' : user_agent, 'Accept' : accept }
		# store the urls to be handled
		self.__openURLs = []
		# openUrls' buffer, wait to be put in openUrls
		self.__readyURLs = []
		# store the finished urls
		self.__closeURLs = []
		# record the page number
		self.__page_num = 0
		# the total page number we want
		self.__total_num = float('inf')

	# load the openURls
	def LoadOpenUrls(self):
		with open('openUrls', 'r') as iinput:
			self.__openURLs = cPickle.load(iinput)

	# load the readyURLs
	def LoadReadyUrls(self):
		with open('readyUrls', 'r') as ipt:
			self.__readyURLs = cPickle.load(ipt)

	# load the closeURLs
	def LoadCloseUrls(self):
		with open('closeUrls', 'r') as ipt:
			self.__closeURLs = cPickle.load(ipt)

	# store the openURLs
	def StoreOpenUrls(self):
		with open('openUrls', 'w') as output:
			cPickle.dump(self.__openURLs, output)

	# store the readyURLs
	def StoreReadyUrls(self):
		with open('readyUrls', 'w') as output:
			cPickle.dump(self.__readyURLs, output)

	# store the closeURLs
	def StoreCloseUrls(self):
		with open('closeUrls', 'w') as output:
			cPickle.dump(self.__closeURLs, output)

	# store the PID
	def StorePageID(self):
		with open('PageID', 'w') as opt:
			cPickle.dump(self.__PID__, opt)

	# get the page and make it analysable
	def __downloadPage(self, url):
		timeout = False
		# download the page
		try:
			r = requests.get(url, headers = self.__headers, timeout = 20)
		except Exception as e:
			timeout = True
			print 'timeout: ' + url
			raise e
		# analyze the page !!! note the difference between r.text and r.content !!!
		raw = btsp(r.content, 'lxml')
		return raw, timeout

	# generate the eligible urls
	# This method must receive one page info, either url or raw. If give it
	# both, it will just handle the url
	def GenerateURLs(self, url = None, raw = None):
		timeout = False
		if url != None:
			raw, timeout = self.__downloadPage(url)

		if timeout:
			return False

		# change the regular expression to suit your need
		lst = raw.find_all("a", href = re.compile(r"http://.*?sina\..*?/2016-12.*?html$"))
			
		for ilst in lst:
			href = ilst['href'].strip()

			pattern = re.compile(r'blog\.|video\.|slide\.')
			# we do not need blog, video and slide
			if re.search(pattern, href):
				continue

			if (href not in self.__readyURLs) and (href not in self.__closeURLs):
				self.__readyURLs.append(href)

		return True

	# generate first open url
	def GenerateHomeUrls(self, url):
		if self.GenerateURLs(url = url):
			self.__openURLs = self.__readyURLs
			self.__readyURLs = []
			self.StoreOpenUrls()
		else:
			print 'cannot download the home page'

	# read n pages, and extract the content, if there is any we want, from the openUrls
	def ReadnPage(self, n):
		self.__total_num = n
		flag = self.__ReadAllPage()
		finished = True

		while not flag:
			if len(self.__readyURLs) == 0:
				print 'sorry, spider cannot find any new page'
				finished = False
				break

			self.__openURLs = self.__readyURLs
			self.__readyURLs = []
			flag = self.__ReadAllPage(load = False)

		if finished:
			print 'mission finished!'

		print 'we have already {0} pages available'.format(self.__page_num)
		print 'ready urls: {0}'.format(len(self.__readyURLs))
		print 'closed urls: {0}'.format(len(self.__closeURLs))

		self.StorePageID()
		self.StoreOpenUrls()
		self.StoreReadyUrls()
		self.StoreCloseUrls()

	# carry on spider's work based on outer urls(open, ready and close)
	def GoOnReadnPage(self, n):
		self.LoadReadyUrls()
		self.LoadCloseUrls()
		# load pid
		with open('PageID', 'r') as ipt:
			self.__PID__ = cPickle.load(ipt)

		self.__page_num = self.__PID__ - 100000

		self.ReadnPage(n + self.__page_num)

	# read all the pages in openUrls, and extract the eligible content from the openUrls
	# parameter 'load' means whether it should load the openUrls' file
	def __ReadAllPage(self, load = True):
		# load pid
		with open('PageID', 'r') as ipt:
			self.__PID__ = cPickle.load(ipt)
		if self.__PID__ >= 200000:
			self.__PID__ = 100000

		if load:
			self.LoadOpenUrls()

		# pdb.set_trace()

		headname = 'sinanews/' + str(datetime.date.today()) + '-'

		with open('pagelog.txt', 'a') as logop:
			for url in self.__openURLs:
				if url in self.__closeURLs:
					# it has already got this page
					continue

				raw, timeout = self.__downloadPage(url)
				if timeout:
					continue
				# Why do these here? I just make it according to the sina html page.
				# Page architecture can be changed over time, thus the codes below
				# can be invalid in some days.
				title = raw.find("title").get_text().strip()
				underline = title.find('_')

				if title != None and underline > -1:
					title = title[0 : underline]
				
				content = raw.find("div", id = "artibody")

				if content == None:
					content = raw.find("div", id = "articleContent")

				if content != None:
					news = ''
					for child in content.descendants:
						# just extract the passage content
						if child.name == u'p':
							news = news + child.get_text().strip()

					# if the text is long enough to be a news
					if len(news) > 100:
						self.__PID__ += 1
						self.__page_num += 1
						print 'page ' + str(self.__page_num) + ': '+ title + '\n' + url + '\n'
						
						# store into log
						filelog = 'page ' + str(self.__page_num) + ': '+ title + '\n' + url + '\n\n'
						logop.write(filelog.encode('utf-8'))

						# store into file
						myname = headname + str(self.__PID__)
						with open(myname, 'w') as iotp:
							iotp.write((title + '\n' + news).encode('utf-8'))

					else:
						print 'too short: ' + url + '\n'

				else:
					print 'nothing: ' + url + '\n'

				# generate new urls
				self.GenerateURLs(raw = raw)
				# store the finished url
				if url not in self.__closeURLs:
					self.__closeURLs.append(url)
				# spider needs to have a rest
				time.sleep(2)
				if self.__page_num >= self.__total_num:
					break

		# store the PID
		self.StorePageID()

		return self.__page_num >= self.__total_num


if __name__ == '__main__':
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
			# raise e