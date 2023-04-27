import random
import tail
import globals
import memray
import numpy as np

# Memory profiling of each function with sequence of length
# sequence_size and a random (valid) n index.
def mem_profile(sequence_size):
	# make sequence all 1's for consistency
	sequence = [1] * sequence_size
	sequence_np = np.ones(sequence_size)
	# for each round
	for _ in range(globals.NUM_ROUNDS):
		n = random.randint(0, sequence_size)
		# profile each function
		for function in tail.functions:	
			if "numpy" in function.__name__:
				function(sequence_np, n)
			else:
				function(sequence, n)
	return
