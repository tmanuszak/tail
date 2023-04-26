import cProfile, pstats, random, os, collections
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
def profile(sequence_size, prof_data):
	# make sequence all 1's for consistency
	sequence = [1] * sequence_size
	# for each round
	for _ in range(NUM_ROUNDS):
		n = random.randint(0, sequence_size)
		# profile each function
		for function in functions:
			filename = "{}.prof".format(function.__name__)
			pf = cProfile.runctx(statement='{}(sequence, n)'.format(function.__name__), 
					globals={'{}'.format(function.__name__): function},
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
	ax.set_title('Plot Title')
	ax.set_xlabel('Sequence Length (log scale)')
	ax.set_ylabel('Running Time (log scale)')
	ax.set_xscale('log', base=10)
	ax.set_yscale('log', base=10)

	plt.savefig('/mnt/c/Users/Trey/Downloads/myplot.png')
	return

if __name__ == "__main__":
	# results[function name] = [running times of funtion]
	prof_data = collections.defaultdict(list)

	sequence_sizes = np.geomspace(1, MAX_SEQ_SIZE, NUM_TRIALS)
	for sequence_size in sequence_sizes:
		prof_data = profile(int(sequence_size), prof_data)
	plot_prof_data(prof_data)

