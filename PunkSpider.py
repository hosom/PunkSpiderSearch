#!/usr/bin/env python
'''
Author  	: 	Stephen Hosom
Last Mod.	: 	07.21.2013
Changelog	: 	07.21.2013 - Creation
Purpose		: 	Provides script access to the PunkSpider search engine.
				Creates python like datatypes to hold the results from
				the search.
'''

__version__ = '0.1.0'

'''
http://punkspider.hyperiongray.com/service/search/domain/

searchkey: url|title
searchvalue: the url or title you would like to search for
pages: 0
pagesize: how many results (10 by default)
pagenumber: which page (1 by default)

working example:
http://punkspider.hyperiongray.com/service/search/domain/?searchkey=url&searchvalue=isc.sans.edu&pages=0&pagesize=10&pagenumber=1
'''

from requests import get
from ast import literal_eval

URL = 'http://punkspider.hyperiongray.com/service/search/domain/'	

def search(**kwargs):
	'''
	Generator function to walk through a search.
	'''

	params = kwargs
	max_pages = PunkSpiderSearch(**params).page_count

	try:
		assert params['pagenumber']
	except KeyError:
		params['pagenumber'] = 1

	while params['pagenumber'] < max_pages:
		yield PunkSpiderSearch(**params)
		params['pagenumber'] += 1


class PunkSpiderSearch(object):
	'''
	Class used to interact with PunkSpider and place results into
	Search.results_list.
	'''

	__params = {}

	def __init__(self, **kwargs):
		'''
		Accepts kwargs to be used as parameters for the search.
		Valid parameters are:
		searchkey: url|title
		searchvalue: the url or title you would like to search for
		pages: 0
		pagesize: how many results (10 by default)
		pagenumber: which page (1 by default)

		ADDITIONALLY, values such as xss=1 may be used to look for 
		only those pages with vulnerabilities.
		'''

		self.__params = kwargs

		results = get(URL, params=self.__params)

		results = literal_eval(results.text)['data']

		self.page_count = results['numberOfPages']
		self.rows_found = results['rowsFound']
		self.results_list = [SearchResult(result) for result 
								in results['domainSummaryDTOs']]
		

class SearchResult(object):
	'''
	Object to hold individual result within a search.
	'''
	
	def __init__(self, summary):
		'''
		Accepts the summary of a search result and creates a data type
		that holds the data within the summary in a convenient format.
		'''
		
		self.id = summary['id']
		self.timestamp = summary['timestamp']
		self.title = summary['title']
		self.url = summary['url']
		self.bsqli = summary['bsqli']
		self.sqli = summary['sqli']
		self.xss = summary['xss']
		self.exploitability_level = summary['exploitabilityLevel']

	def __str__(self):
		'''
		Creates a string object of the search result.
		'''

		return '''
id: %s
timestamp: %s
title: %s
url: %s
bsqli: %s
sqli: %s
xss: %s
exploitability level: %s''' % (self.id, self.timestamp, self.title, 
								self.url, self.bsqli, self.sqli, 
								self.xss, self.exploitability_level)
