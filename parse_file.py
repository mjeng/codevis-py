import requests
import json
import re

def create_graph(file_list):
	file_functions={} #dictionary of all files to list of functions that shit has

	#fills up file_functions
	for curr_file in file_list:
		#with open(curr_file) as f:
			#file_functions[curr_file]=get_functions(f)
		file_functions[curr_file]=get_functions(f)

#get passed in iterable of all lines in file
def get_functions(file_string):
	func_list = re.findall(r'def \w*:', file_string)
	return [func_line[func_line.find(" ")+1:func_line.find(":")] for func_line in func_list]
