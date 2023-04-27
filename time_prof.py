import cProfile, pstats, random, os
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tail
import globals

# Returning trials-many running times of each function with sequence of 
# total_numbers ints and a random (valid) n.
def profile(sequence_size, prof_data):
	# make sequence all 1's for consistency
	sequence = [1] * sequence_size
	sequence_np = np.ones(sequence_size)
	# for each round
	for _ in range(globals.NUM_ROUNDS):
		n = random.randint(0, sequence_size)
		# profile each function
		for function in tail.functions:
			filename = f"{function.__name__}.prof"
			# if sequence is numpy or not
			pf = None
			if function == tail.functions[-1]:
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
	arr = np.repeat(
		np.geomspace(1, globals.MAX_SEQ_SIZE, globals.NUM_TRIALS), 
		globals.NUM_ROUNDS)
	df['x'] = np.concatenate((arr,) * len(tail.functions)) 
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

	plt.savefig('./time-profile-plot1.png')
	return
