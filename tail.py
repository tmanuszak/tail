import cProfile, pstats, random, os, collections

# simple slice
def tail_v1(sequence, n):
	return sequence[-n:]

# append one by one
def tail_v2(sequence, n):
	result = []
	for i in range(-n, 0):
		result.append(sequence[i])
	return result

# name of functions that are profiled
functions = [tail_v1, tail_v2]

# Returning trials-many running times of each function with sequence of 
# total_numbers ints and a random (valid) n.
def profile(total_numbers: int, trials: int):
	# will be returned
	# results[function name] = [running times of each trial]
	results = collections.defaultdict(list)

	# make sequence all 1's for consistency
	sequence = [1] * total_numbers

	# profile each function trials-many times
	for trial in range(trials):
		# make n a random valid index
		n = random.randint(0, total_numbers)
		# profile each function
		for function in functions:
			filename = "{}_{}.prof".format(function.__name__, trial)
			pf = cProfile.runctx(statement='{}(sequence, n)'.format(function.__name__), 
					globals={'{}'.format(function.__name__): function},
					locals={'sequence': sequence, 'n': n},
					filename=filename)
			stats = pstats.Stats(filename)
			results[function.__name__].append(stats.total_tt)
			os.remove(filename)
	return results

def add_prof_data_to_graph(current_graph, prof_data):
	return NotImplementedError

if __name__ == "__main__":
	trials = 50  # number of trials for each exponent below
	# testing arrays up to size 3.6 GB 
	for exponent in range(9):
		prof_data = profile(10**exponent, trials)

