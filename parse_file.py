import requests
import json
import re
import utils
import create_graph as cg
from heapq import heappush, heappop

class CallData:
	def __init__(self,func_name,src_file,call_list,times_called):
		self.func_name=func_name
		self.src_file=src_file
		self.call_list=call_list
		self.times_called=times_called
	def get_func_name(self):
		return self.func_name
	def get_src_file(self):
		return self.src_file
	def get_call_list(self):
		return self.call_list
	def get_times_called(self):
		return self.times_called
	def set_func_name(self,f):
		self.func_name=f
	def set_src_file(self,s):
		self.src_file=s
	def set_call_list(self,cl):
		self.call_list=cl
	def set_times_called(self,tc):
		self.times_called=tc




def gh_link_entry(link):
	get_filemap_tuple=utils.get_filemap(link)
	dict = get_filemap_tuple[0]
	granularity=5

	keys = list(dict.keys())
	create_graph_ret_tuple=create_graph(keys, dict)

	connections=create_graph_ret_tuple[0]
	line_counts=create_graph_ret_tuple[1]
	name_to_CD=create_graph_ret_tuple[2]

	#call recursive func
	if((granularity is not None) and granularity<=len(connections)):
		connections=[(-1*get_function_weight(c,line_counts,name_to_CD),c) for c in connections]
		heap=[]
		for elem in connections:
			heappush(heap,elem)
		print(heap)
		connections=heap[0:granularity]
		connections=[elem[1]for elem in connections]
	cg.draw(connections)
	return connections


def get_function_weight(single_cnct,lc,n2cd):#single connection, line_counts
	if len(single_cnct.get_call_list())==0:
		return lc[single_cnct.get_func_name()]
	else:
		return lc[single_cnct.get_func_name()] + sum([get_function_weight(n2cd[x],lc,n2cd) for x in single_cnct.get_call_list()])

########
# file_list --> list of file ID's
# src_code_dict --> dictionary of file ID's to the actual fat src code string
#######
def create_graph(file_list,src_code_dict):
	file_functions={} #dictionary of all file ID's to list of functions that shit has
	all_functions={} #set of all functions
	line_count={}# set of all functions mapped to their line counts
	name_to_CD={}# dict of func name mapped to cd obj

	#fills up file_functions. After this for loop, you get dict of src file names with list of funcs in it
	for curr_file in file_list:
		file_functions[curr_file]=get_functions(src_code_dict[curr_file])
		#after we get returned a list from above function call, we add to the set below
		for elem in file_functions[curr_file]:
			all_functions[elem]=0
			line_count[elem]=0
	#print(all_functions.keys())
	# creates CallData objects for all funcs
	call_data_objects=[]
	for src_key in file_functions:
		src_file=src_code_dict[src_key]
		curr_src_split=src_file.split("\n")#essentially makes raw file into lines of a txt file
		curr_funcs=file_functions[src_key]
		#print(len(curr_src_split))
		#print(curr_funcs)

		for func in curr_funcs:
			curr_search="def "+func #just in case u call this function above the def

			curr_call_list=[]

			#get to next def
			while curr_src_split!=[] and curr_src_split !=[''] and curr_search not in curr_src_split[0]:
				curr_src_split=curr_src_split[1:]
			curr_src_split=curr_src_split[1:]

			while curr_src_split !=[] and (curr_src_split[0]=='' or curr_src_split[0][0]==" "): #check if space is first char to make sure actually under def
				line_count[func]+=1
				for funcs in all_functions:
					funcs1=funcs+"("
					if funcs1 in curr_src_split[0]:#can always make it like curr_search later
						curr_call_list.append(funcs)#potentially could call same func multiple times. Maybe in future implement counter, and make arrow thi
						all_functions[funcs]+=1
				curr_src_split=curr_src_split[1:]

			call_data_objects.append(CallData(func,src_key,curr_call_list,0))


	for o in call_data_objects:
		o.set_times_called(all_functions[o.get_func_name()])
		name_to_CD[o.get_func_name()]=o

	return (call_data_objects,line_count,name_to_CD)

#get passed in iterable of all lines in file
def get_functions(file_string):
	#func_list = re.findall(r'def \w*:', file_string)
	#return [func_line[func_line.find(" ")+1:func_line.find(":")] for func_line in func_list]
	ret=[]
	curr_src_split=file_string.split("\n")
	for line in curr_src_split:
		if line[0:3] == "def":
			ret.append(line[line.find(" ")+1:line.find("(")])
		if line[0:3] != "def" and ("def" in line):
			ret.append(line[line.find("def")+4:line.find("(")])

	return ret
