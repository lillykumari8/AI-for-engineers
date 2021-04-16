from ai_hw1 import State, recursive_dfs

def main():
	"""defining the initial State of the problem"""
	initial_state = State(3,3,"L")
	recursive_dfs(initial_state, [])

if __name__ == "__main__":
	main()