#!/usr/bin/env python
'''
Author  	: 	Stephen Hosom
Last Mod.	: 	07.21.2013
Changelog	: 	07.21.2013 - Creation
Purpose		: 	Performs command line searches of the PunkSpider
				search engine.
'''

__version__ = '0.1.0'

from argparse import ArgumentParser
from PunkSpider import search
from csv import writer

def get_args():
	'''
	Accepts no arguments and uses sys.argv for input.
	Uses ArgumentParser to parse command line arguments and options.
	Returns an object that describes all arguments and options 
	that were passed to the script.
	'''

	parser = ArgumentParser()

	# Only required value
	parser.add_argument('searchvalue', action='store', type=str,
						help='The value to search for.')

	parser.add_argument('-k', '--searchkey', type=str,
						action='store', dest='searchkey',
						choices=['url', 'title'], 
						default='url', 
						help='Search on the title, or the url of \
								the page. Must be set to title or url')
	parser.add_argument('-C', '--csvoutput', type=str,
						action='store', dest='output_location', 
						default=None,
						help='Switch to CSV output and save at the \
								location specified.')

	# Flags to only include results with positives
	parser.add_argument('-x', '--xss', action='store_true', dest='xss',
							default=None,						
							help='Include only XSS positives.')
	parser.add_argument('-b', '--bsqli', action='store_true', 
						dest='bsqli', default=None,
						help='Include only BSQLI positives.')
	parser.add_argument('-s', '--sqli', action='store_true', 
						dest='sqli', default=None,
						help='Include only SQLI positives.')

	args = parser.parse_args()
	return args

def process_args(args):
	'''
	Accepts an ArgumentParser.parse_args() return object as its only
	parameter. Performs some logic on the arguments passed to the 
	script and then returns the formatted dictionary for the search.
	'''

	# Dictionary to hold search parameters
	params = {'searchkey': args.searchkey, 
				'searchvalue': args.searchvalue}

	if args.bsqli is not None:
		params['bsqli'] = 1
	if args.xss is not None:
		params['xss'] = 1
	if args.sqli is not None:
		params['sqli'] = 1

	return params

def results_generator(params):
	'''
	Accepts a dictionary as an argument and then performs a search
	on PunkSpider for those parameters specified in the dictionary.
	Yields one search result per. 
	'''

	for page in search(**params):
		for result in page.results_list:
			yield result

def write_csv(output_location, params):
	'''
	Accepts an output location and parameters for the search as
	input. Performs the search and then writes the output to a csv.
	'''

	rows = [[result.id, result.timestamp, result.title,
				result.url, result.bsqli, result.sqli, result.xss] 
					for result in results_generator(params)]

	titles = ['ID', 'TIMESTAMP', 'TITLE', 'URL', 'BSQLI', 'SQLI', 
				'XSS']
	rows.insert(0, titles)

	with open(output_location, 'wb') as f:
		csvwriter = writer(f)		
		csvwriter.writerows(rows)

def main():
	'''
	Reads user input, processes the user input, and then looks up
	results for the corresponding search on PunkSpider.
	'''

	args = get_args()

	params = process_args(args)

	if args.output_location is not None:
		write_csv(args.output_location, params)
	else:
		for result in results_generator(params):
			print result


if __name__ == '__main__':
	main()
