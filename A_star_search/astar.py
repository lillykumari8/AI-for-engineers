import sys
import math


class Node():
	'''
	Defining Node with the following attributes:
	state: a tuple denoting x,y coordinates - example - (0, 0)
	parent: parent(node object) of the node
	successors: list of successor nodes
	h_value: its distance from the goal node(state)
	g_value: sum of edge costs from start state to current node
	f_value: sum of node's h_value & g_value
	'''

	def __init__(self, state, parent):
		self.state = state
		self.parent = parent
		self.successors = []
		self.h_value = 0.0
		self.g_value = 0.0
		self.f_value = 0.0

	def update_node(self, other):
		'''args - node1, node2
		modifies the node1 by using attribute values corres. to node2'''
		self.parent = other.parent
		self.successors = other.successors
		self.g_value = other.g_value
		self.h_value = other.h_value
		self.f_value = other.f_value

	def __eq__(self, other):
		'''Overriding the default object equality method so that it does not do memory refernce based comparison
		but instead compare the properties. This will be used to check if a node exists in list'''
		return self.state == other.state


def get_distance(state_a, state_b):
	'''helper function to calculate distance between 2 states
	Args - 2 state values in the form of (x, y)
	Returns the euclidean distance between them'''
	vec1 = ([state_a[0], state_a[1]])
	vec2 = ([state_b[0], state_b[1]])
	dist = math.sqrt(sum([(a - b) ** 2 for a, b in zip(vec1, vec2)]))
	return dist


'''the line segment intersection algorithm is taken from: 
	https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/'''
def on_segment(p, q,r) :
	'''Args - 3 collinear states(points) in the form of tuple (x, y)
	Checks if point q lies on line segment pr'''
	if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and \
		q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
		return True
	return False


def orientation(p, q, r):
	'''function to find the orientation of the ordered triplet of 3 points
	Args - 3 collinear states(points) in the form of tuple (x, y)
	Returns 0 if p,q,r are collinear, 1 if orientation is clockwise, 2 if orientation is counter-clockwise'''
	val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
	if (val == 0):
		return 0
	elif (val>0):
		return 1
	else:
		return 2


def do_intersect(p1, q1, line_segment):
	'''function to check if a line segment (edges of rectangles) intersects a line segment 
	formed by 2 points - current node to next node
	Args - p1(state of current node), q1(state of next node), line segment
	Returns True if line_segment intersects with the line segment formed by p1, q1'''
	p2 = line_segment[0]
	q2 = line_segment[1]

	o1 = orientation(p1, q1, p2)
	o2 = orientation(p1, q1, q2)
	o3 = orientation(p2, q2, p1)
	o4 = orientation(p2, q2, q1)
	if (o1 != o2 and o3 != o4):
		return True
	elif (o1 == 0 and on_segment(p1, p2, q1)):
		return True
	elif (o2 == 0 and on_segment(p1, q2, q1)):
		return True
	elif (o3 == 0 and on_segment(p2, p1, q2)):
		return True
	elif (o4 == 0 and on_segment(p2, q1, q2)):
		return True
	else:
		return False


def is_odd(num):
	'''a helper function to check whether a number is odd or not'''
	if num%2 != 0:
		return True


def print_path(visited_nodes):
	'''A helper method to print the content of the visited_nodes which is a list object'''
	dash = '-' * 65
	if visited_nodes:
		print dash
		print '{:<10s}{:<16s}{:>12s}{:>14s}'.format("Point", "Cumulative Cost (g)", "h_value", "f_value")
		print dash
		for node in visited_nodes:
			print '{:<10s}{:>12.5f}{:>18.5f}{:>18.5f}'.format("(" + str(node.state[0]) + ',' + str(node.state[1]) + ")", node.g_value, node.h_value, node.f_value)


def get_lowest_cost_node_from_openlist(open_list):
	'''helper function to retrieve the node (& its index) with lowest f_value from the open_list'''
	
	# assigning the first open_list node as best_node
	best_node = open_list[0]
	best_index = 0
	# assigning the node in open_list with lowest f_value as the best_node & its index as best_index
	for index, node in enumerate(open_list):
		if node.f_value < best_node.f_value:
			best_node = node
			best_index = index
	return best_index, best_node


def get_successors(best_node, states_dict, line_segments):
	# generating successors of the best_node
	successors = []
	for st in states_dict.keys():
		if st != best_node.state:
			intersect_count = 0
			# taking care of the case in which traversal along an edge (best_node, st) of a rectangle which intersects with another edge of that rectangle
			# can be accepted as a possible move (i.e. move to an adjoining vertex in which checking the sum of vertix number for "odd"ness helps)
			if states_dict[st]['rect'] == states_dict[best_node.state]['rect'] and is_odd(states_dict[st]['vertex']+states_dict[best_node.state]['vertex']):
				successors.append(st)
				continue
			# checking if the line segment formed by best_node & st intersects with the existing edges (which does not contain
			# either best_node or st) of rectangles in the environment
			for line_seg in line_segments:
				if do_intersect(best_node.state, st, line_seg):
					if best_node.state not in line_seg and st not in line_seg:
						intersect_count += 1
						break
			# intersect_count == 0 means that the possible line segment doesnt intersect with any edges, hence we add
			# that state (coordinates) to the successors list
			if intersect_count==0:
				if st not in successors:
					if states_dict[st]['rect']!=states_dict[best_node.state]['rect']:
						successors.append(st)
	return successors


def astar_search(start, end, states_dict, line_segments):
	'''the astar_search algorithm which takes the following args:
	start: the starting state(coordinates)
	end: the goal state(coordinates)
	states_dict: a dictionary object which stores the different states in the search alongwith their rectangle & vertex reference
	line_segments: a list of list of two states which represent the edges of different rectangles in the space
	Returns a list of node objects which should be traversed inorder to get the shortest path from start to end'''

	# initializing an open list which stores nodes which haven't been expanded
	open_list = []
	# initializing a closed_list which stores nodes which have been expanded
	closed_list = []

	# assigning the start_node with given start state with its parent as None
	start_node = Node(start, None)
	# assigning the end_node with given end state with its parent as None
	end_node = Node(end, None)

	start_node.g_value = 0
	start_node.h_value = get_distance(start_node.state, end_node.state)
	start_node.f_value = start_node.g_value + start_node.h_value

	# appending start_node to the open_list
	open_list.append(start_node)

	# continue until the open list becomes empty
	while len(open_list) > 0:

		# getting the best_node with lowest f_value from the open_list
		best_index, best_node = get_lowest_cost_node_from_openlist(open_list)

		# removing best_node from open_list & adding it to the closed_list
		open_list.pop(best_index)
		closed_list.append(best_node)

		# if best_node is the goal node, we populate the shortest path in a list & return
		if best_node == end_node:
			possible_path = []
			current = best_node
			while current is not None:
				possible_path.append(current)
				current = current.parent
			possible_path.reverse()
			return possible_path

		# generating successors of the best_node
		successors = get_successors(best_node, states_dict, line_segments)

		for succ in successors:
			# assigning a node object using the succ state & setting its parent to best_node
			new_node = Node(succ, parent=best_node)
			# setting remaining attributes (distance/cost parameters)
			new_node.g_value = best_node.g_value + get_distance(succ, best_node.state)
			new_node.h_value = get_distance(succ, end_node.state)
			new_node.f_value = new_node.g_value + new_node.h_value

			# finding if the state of new_node already exists in any of the open_list or closed_list
			common_open = [i for i in range(len(open_list)) if open_list[i]==new_node]
			common_closed = [i for i in range(len(closed_list)) if closed_list[i]==new_node]

			# if same state exists in open_list as o_node, add o_node to successors of best_node 
			if len(common_open) > 0:
				o_node = open_list[common_open[0]]
				best_node.successors.append(o_node)
				# if new_node's f_value is less, then we update the o_node in the open_list
				if new_node.f_value < o_node.f_value:
					open_list[common_open[0]].update_node(new_node)

			# if same state exists in closed_list as c_node, add c_node to successors of best_node 
			elif len(common_closed) > 0:
				c_node = closed_list[common_closed[0]]
				best_node.successors.append(c_node)
				# if new_node's f_value is less, then we update the c_node in the closed_list, add it 
				# to the open_list & remove it from the closed_list
				if new_node.f_value < c_node.f_value:
					closed_list[common_closed[0]].update_node(new_node)
					open_list.append(closed_list[common_closed[0]])
					closed_list.pop(common_closed[0])

			else:
				# if state not in open_list and closed_list, add its node to the open_list & to the successors of best_node
				open_list.append(new_node)
				best_node.successors.append(new_node)

	print 'Open List is empty'


def read_file(filename):
	'''utility function for reading the input file
	Args: filename
	Returns start - (x,y) tuple object, 
	end - (x,y) tuple object, 
	states_dict - a dictionary object which stores the different states (as keys) in the search alongwith their rectangle & vertex number
		Example - {(0,0): {'rect':0, 'vertex':0}, (4,0): {'rect':0, 'vertex':1},......}
	line_segments: a list of list of two states which represent the edges of different rectangles in the environment
		Example - [[(0,0), (4,0)], [(4,0), (4,4)], .....]
	'''
	with open(filename, 'r') as f:
		lines = f.readlines()
	# if file not empty
	if len(lines)>0:
		states_dict = {}
		line_segments = []
		line0 = lines[0].strip().split(' ')
		start = (int(line0[0]), int(line0[1]))
		line1 = lines[1].strip().split(' ')
		end = (int(line1[0]), int(line1[1]))

		# rect_c - number representing the order in which rectangles are given in input file
		# vertex_c - number representing the vertex order of a rectangle in a clockwise manner
		rect_c = 0
		for line in lines[3:]:
			line = line.strip().split(' ')
			vertex_c = 0
			coords = [(int(line[0]), int(line[1])), (int(line[2]), int(line[3])), (int(line[4]), int(line[5])) ,(int(line[6]), int(line[7]))]
			for co in coords:
				states_dict[co] = {}
				states_dict[co]['rect'] = rect_c
				states_dict[co]['vertex'] = vertex_c
				vertex_c += 1

			rect_c += 1

			for i in range(len(coords)-1):
				line_segments.append([coords[i], coords[i+1]])
			line_segments.append([coords[3], coords[0]])

		return start, end, states_dict, line_segments

	else:
		print 'File is empty'