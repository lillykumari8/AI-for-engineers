import os
from astar import *

def main():
	
	cwd = os.getcwd()
	file_list = []
	file_list.append(cwd + '/simple_dataset.txt')
	file_list.append(cwd + '/difficult_dataset.txt')
	file_list.append(cwd + '/customized_dataset.txt')
	for file in file_list:
		start, end, states_dict, line_segments = read_file(file)
		path = astar_search(start, end, states_dict, line_segments)
		file_name = file.split('/')[-1][:-4]
		print 'Solution for', file_name
		print_path(path)
		print '\n'


if __name__=="__main__":
	main()