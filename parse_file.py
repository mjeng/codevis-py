import requests
import json
import re

class CallData:
	def __init__(self,func_name,src_file,call_list):
		self.func_name=func_name
		self.src_file=src_file
		self.call_list=call_list
	def get_func_name(self):
		return self.func_name
	def get_src_file(self):
		return self.src_file
	def get_call_list(self):
		return self.call_list
	def set_func_name(f):
		self.func_name=f
	def set_src_file(s):
		self.src_file=s
	def set_call_list(cl):
		self.call_list=cl

########
# file_list --> list of file ID's
# src_code_dict --> dictionary of file ID's to the actual fat src code string
#######
def create_graph(file_list,src_code_dict):
	file_functions={} #dictionary of all file ID's to list of functions that shit has
	all_functions={} #set of all functions

	#fills up file_functions. After this for loop, you get dict of src file names with list of funcs in it
	for curr_file in file_list:
		file_functions[curr_file]=get_functions(src_code_dict[curr_file])
		#after we get returned a list from above function call, we add to the set below
		for elem in file_functions[curr_file]:
			all_functions[elem]=1
	#print(file_list)
	# creates CallData objects for all funcs
	call_data_objects=[]
	for src_key in file_functions:
		src_file=src_code_dict[src_key]
		#print(src_file)
		curr_src_split=src_file.split("\n")#essentially makes raw file into lines of a txt file
		curr_funcs=file_functions[src_key]
		#print(curr_src_split)
		for func in curr_funcs:
			curr_search="def "+func+":" #just in case u call this function above the def
			curr_call_list=[]

			#get to next def
			while curr_search not in curr_src_split[0]:
				curr_src_split=curr_src_split[1:]
			curr_src_split=curr_src_split[1:]

			while curr_src_split !=[] and curr_src_split != [''] and curr_src_split[0][0]==" ": #check if space is first char to make sure actually under def
				for funcs in all_functions:
					if funcs in curr_src_split[0]:#can always make it like curr_search later
						curr_call_list.append(funcs)#potentially could call same func multiple times. Maybe in future implement counter, and make arrow thi
				curr_src_split=curr_src_split[1:]

			call_data_objects.append(CallData(func,src_file,curr_call_list))

	return call_data_objects[0].get_call_list()
#get passed in iterable of all lines in file
def get_functions(file_string):
	func_list = re.findall(r'def \w*:', file_string)
	return [func_line[func_line.find(" ")+1:func_line.find(":")] for func_line in func_list]

testDict={"src1":"def a:\n  b() \n  c()\nc()\ndef b:\ndef c:"}
testStr=["src1"]
print(create_graph(testStr,testDict))
