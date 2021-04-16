################################################################
# AUTHOR - Lilly Kumari, UWNetID - lkumari@uw.edu
# AIM - to print possible solutions for the missionary cannibal problem using Recursive DFS
# INITIAL STATE - (3,3,L) - where first part of tuple - number of missionaries on Left side of bank,
# second part of tuple - number of cannibals on left side of bank, third part of tuple - position of boat
# OUTPUT - prints existing solution paths & count of illegal_states, repeated_states & total_states checked
################################################################

"""declaring following Global variables:
	repeated_states: an int for tracking the states which have been visited.
	illegal_states: an int for tracking the illegal states encountered during overall search.
	total_states: an int for tracking all states except illegal states visited during search.
"""
repeated_states = 0
illegal_states = 0
"""Initialising total_states with 1 since we are starting the recursion with root (initial_state) and hence already marking it counted
   This variable will help us calculate the total states.
"""
total_states = 1

class State():
	""" defining State with the following attributes:
		missionaries: an int tracking the number of missionaries on the left side of the bank.
		cannibals: an int tracking the number of cannibals on the left side of the bank.
		boat_shore: a string tracking the position (shore- Left (L) or Right (R)) of the boat
	"""
	def __init__(self, missionaries, cannibals, boat_shore):
		"""Returns a State object with its attributes """
		self.missionaries = missionaries
		self.cannibals = cannibals
		self.boat_shore = boat_shore

	def is_target(self):
		"""Returns a boolean value for whether the input state is the target state or not"""
		if self.missionaries == 0 and self.cannibals == 0 and self.boat_shore == "R":
			return True
		else:
			return False

	def is_legal(self):
		"""Returns a boolean value specifying whether the input state is legal or not (illegal when cannibals eat the missionaries)"""
		if (self.missionaries >= self.cannibals or self.missionaries == 0) \
			and (self.cannibals >= self.missionaries or self.missionaries == 3):
			return True
		else:
			return False

	def is_valid(self):
		"""Returns a boolean value whether the input state is satisfying the number constraints or not"""
		if self.missionaries >=0 and self.missionaries <= 3 \
			and self.cannibals >=0 and self.cannibals <= 3:
			return True
		else:
			return False

	def get_successors(self):
		"""* Returns a list of successors for a given input state object based on qualifying criteria of being a valid
		   and legal state.
		   * have defined the possible actions in action_list
		   * It also tracks the illegal_states encountered while state generation and traversal"""
		successors = []
		global illegal_states
		"""(1,0) - when 1M moves, (0,1) - 1C moves, (2,0) - 2M move, (0,2) - 2C move, (1,1) - 1M and 1C move"""
		action_list = [(1,0), (0,1), (2,0), (0,2), (1,1)]
		if self.boat_shore == "L":
			for act in action_list:
				"""subtracting since M or/and C moving to right shore"""
				potential_next_state = State(self.missionaries - act[0], self.cannibals - act[1], "R")
				if potential_next_state.is_valid():
					if potential_next_state.is_legal():
						successors.append(potential_next_state)
					else:
						"""Since this is an illegal node, increment the global variable count"""
						illegal_states += 1
		else:
			for act in action_list:
				"""adding since M or/and C moving to left shore"""
				potential_next_state = State(self.missionaries + act[0], self.cannibals + act[1], "L")
				if potential_next_state.is_valid():
					if potential_next_state.is_legal():
						successors.append(potential_next_state)
					else:
						"""Since this is an illegal node, increment the global variable count"""
						illegal_states += 1
		return successors

	def __eq__(self, other):
		"""Overriding the default object equality method so that it does not do memory refernce based comparison
		but instead compare the properties. This will be used to check if an object exists in list"""
		if self.missionaries == other.missionaries and self.cannibals == other.cannibals and self.boat_shore == other.boat_shore:
			return True

	def __str__(self):
		"""Overiding to Object.ToString() so that when we print object(state in this case); it does not print the 
		memory reference, but instead prints the contents that we need."""
		return "(" + str(self.missionaries) + ',' + str(self.cannibals) + ',' + str(self.boat_shore) + ")"


def print_path(visited_states):
	"""A helper method to print the content of the visited_states"""
	print "Solution: "
	for state in visited_states:
		print state


def recursive_dfs(root, visited_states):
	"""Recursive depth first search to solve the given problem"""
	if root is None:
		return

	"""If we have reached the target state, print the path and return"""
	if root.is_target():
		visited_states.append(root)
		print_path(visited_states)
		visited_states.pop()
		return

	"""Check if the current state is already visited, if yes dont traverse further, and add 1 to the repeated_states count"""
	if root in visited_states:
		global repeated_states
		repeated_states += 1
		return
	else:
		visited_states.append(root)

	"""Recursively call DFS on all the successors of the root to check if any of them reaches the target state"""
	for succ in root.get_successors():
		global total_states
		total_states += 1
		recursive_dfs(succ, visited_states)

	"""Since the subtreee at the root has been fully covered, remove it from visited node"""
	visited_states.pop()

	"""If visited_states list is empty, it means that the recursion has ended, and hence print the required counts"""
	if len(visited_states) == 0:
		"""The final total states = total_states minus the repeated_states (which were skipped)"""
		print "Total Count = ", total_states - repeated_states
		print "Illegal Count = ", illegal_states
		print "Repeat Count = ", repeated_states