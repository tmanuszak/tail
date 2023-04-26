import cProfile, pstats, random, os
from collections import deque, defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import seaborn as sns

# GLOBALS
NUM_TRIALS = 100  # number of trials
NUM_ROUNDS = 10  # number of rounds with randomized n in each trial
MAX_SEQ_SIZE = 10 ** 8

# simple slice
def tail_slicing(sequence, n):
	return sequence[-n:]

# append one by one
def tail_appending(sequence, n):
	result = []
	for i in range(-n, 0):
		result.append(sequence[i])
	return result

# List comp
def tail_list_comp(sequence, n):
	return [sequence[-i] for i in range(n, 0, -1)]

# Deque for fun
def tail_deque(sequence, n):
	return deque(sequence, maxlen=n)

# a space efficient generator for sequence. ONLY USE IF SEQUENCE WONT CHANGE AFTER CALL!
def tail_return_generator(sequence, n):
	def generator():
		index = n + 1
		while index > 1:
			index -= 1
			yield sequence[-index]
	return generator()

# Similar to tail_v5, but returns a list rather than generator. Params are safe to change.
def tail_generator_plus_list(sequence, n):
	def generator():
		index = n + 1
		while index > 1:
			index -= 1
			yield sequence[-index]
	return list(generator())

# called if sequence is an np array.
# Same implementation as v1. Just done this way due to plot implementation.
def tail_numpy_slicing(sequence, n):
	return sequence[-n:]

# name of functions that are profiled
functions = [tail_slicing, tail_appending, tail_list_comp, tail_deque, 
	tail_return_generator, tail_generator_plus_list, tail_numpy_slicing]

# Returning trials-many running times of each function with sequence of 
# total_numbers ints and a random (valid) n.
def profile(sequence_size, prof_data):
	# make sequence all 1's for consistency
	sequence = [1] * sequence_size
	sequence_np = np.ones(sequence_size)
	# for each round
	for _ in range(NUM_ROUNDS):
		n = random.randint(0, sequence_size)
		# profile each function
		for function in functions:
			filename = f"{function.__name__}.prof"
			# if sequence is numpy or not
			pf = None
			if function == functions[-1]:
				pf = cProfile.runctx(
					statement=f'{function.__name__}(sequence, n)', 
					globals={f'{function.__name__}': function},
					locals={'sequence': sequence_np, 'n': n},
					filename=filename)
			else:
				pf = cProfile.runctx(
					statement=f'{function.__name__}(sequence, n)', 
					globals={f'{function.__name__}': function},
					locals={'sequence': sequence, 'n': n},
					filename=filename)
			stats = pstats.Stats(filename)
			prof_data[function.__name__].append(stats.total_tt)
			os.remove(filename)
	return prof_data

def plot_prof_data(prof_data):
	# Convert defaultdict to pandas DataFrame
	df = pd.DataFrame(prof_data) 
	# Reshape the DataFrame so that each row corresponds to an (x, y, function) tuple
	df = pd.melt(df, var_name='function', value_name='y', ignore_index=False)

	# Add an 'x' column to the DataFrame for seq size
	arr = np.repeat(np.geomspace(1, MAX_SEQ_SIZE, NUM_TRIALS), NUM_ROUNDS)
	df['x'] = np.concatenate((arr,) * len(functions))

	# Create the plot with y-axis on a logarithmic scale
	fig, ax = plt.subplots(figsize=(12, 8))
	n_colors = len(df['function'].unique())
	colors = plt.get_cmap('gist_rainbow')(np.linspace(0, 1, n_colors))
	for i, (function, group) in enumerate(df.groupby('function')):
		x, y = group['x'], group['y']
		sns.lineplot(x=x, y=y, label=function)

	# plot metadata
	ax.legend()
	ax.set_title('Running Time Profiles of Tail Functions (Intel i7-7700K @ 4.2GHz)')
	ax.set_xlabel('Sequence Length (log scale)')
	ax.set_ylabel('Running Time (log scale)')
	ax.set_xscale('log', base=10)
	ax.set_yscale('log', base=10)

	plt.savefig('/mnt/c/Users/Trey/Downloads/myplot.png')
	plt.savefig('./time-profile-plot.png')
	return

if __name__ == "__main__":
	# results[function name] = [running times of funtion]
	prof_data = defaultdict(list)

	sequence_sizes = np.geomspace(1, MAX_SEQ_SIZE, NUM_TRIALS)
	for sequence_size in sequence_sizes:
		prof_data = profile(int(sequence_size), prof_data)
	plot_prof_data(prof_data)

