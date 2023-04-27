from collections import defaultdict
import numpy as np
import tail
from time_prof import profile, plot_prof_data
import globals

if __name__ == "__main__":
	# results[function name] = [running times of funtion]
	prof_data = defaultdict(list)

	sequence_sizes = np.geomspace(1, globals.MAX_SEQ_SIZE, globals.NUM_TRIALS)
	for sequence_size in sequence_sizes:
		prof_data = profile(int(sequence_size), prof_data)
	plot_prof_data(prof_data)
