import requests
import json
import re

class CallData:
	def __init__(self,func_name,src_file,call_list):
		self.func_name=func_name
		self.src_file=src_file
		self.call_list=call_list
	def get_func_name:
		return self.func_name
	def get_src_file:
		return self.src_file
	def get_call_list:
		return self.call_list
	def set_func_name(f):
		self.func_name=f
	def set_src_file(s):
		self.src_file=s
	def set_call_list(cl):
		self.call_list=cl

def create_graph(file_list):
	file_functions={} #dictionary of all files to list of functions that shit has
	all_functions={} #set of all functions

	#fills up file_functions. After this for loop, you get dict of src file names with list of funcs in it
	for curr_file in file_list:
		file_functions[curr_file]=get_functions(curr_file)
		for elem in file_functions[curr_file]:
			all_functions[elem]=1

	# creates CallData objects for all funcs
	call_data_objects=[]
	for src_file in file_funcions:
		curr_src_split=src_file.split("\n")#essentially makes raw file into lines of a txt file
		#curr_def_ind = [index for index, value in enumerate(l) if value == "def"] #get all occurences of def in this curr src file. Possibly sus with ==
		curr_funcs=file_functions[src_file]
		for func in curr_funcs:
			curr_search="def "+func+":" #just in case u call this function above the def
			curr_call_list=[]
			while  not in curr_src_split[0]:
				curr_src_split=curr_src_split[1:]

			for i in range(curr_def_ind[0]+1,curr_def_ind[0]):
				if(curr_src_split[i] in all_functions):
					curr_call_list.append(curr_src_split[i]) #potentially could call same func multiple times. Maybe in future implement counter, and make arrow thicker
			call_data_objects.append(CallData(func,src_file,curr_call_list));
			curr_def_ind=curr_def_ind[1:]



#get passed in iterable of all lines in file
def get_functions(file_string):
	func_list = re.findall(r'def \w*:', file_string)
	return [func_line[func_line.find(" ")+1:func_line.find(":")] for func_line in func_list]
