from collections import defaultdict
import os
import numpy as np
import pandas as pd
import dataframe_image as dfi
import matplotlib as plt
import tail
from time_prof import time_profile, plot_prof_data
from mem_prof import mem_profile
import globals
import sys
import memray
import subprocess

if __name__ == "__main__":
	args = set(sys.argv[1:])
	if "time" in args:
		# results[function name] = [running times of funtion]
		prof_data = defaultdict(list)

		sequence_sizes = np.geomspace(1, globals.MAX_SEQ_SIZE, globals.NUM_TRIALS)
		for sequence_size in sequence_sizes:
			prof_data = time_profile(int(sequence_size), prof_data)
		plot_prof_data(prof_data)
	
	if "memory" in args:
		# remove old data file
		try:
			os.remove("mem_data.bin")
		except Exception:
			pass

		# generate sequence_sizes to test
		sequence_sizes = np.geomspace(1, globals.MAX_SEQ_SIZE, globals.NUM_TRIALS)
		
		# do the profiling
		with memray.Tracker("mem_data.bin", memory_interval_ms=1,
			trace_python_allocators=True,
			native_traces=True):
			for sequence_size in sequence_sizes:
				mem_profile(int(sequence_size))
		
		# processing the profile data
		data = defaultdict(list)
		function_names = set(map(lambda f: f.__name__, tail.functions))
		output = subprocess.check_output(
			'python3 -m memray summary -r 1000 mem_data.bin ' \
			'| grep "tail.py"', 
			shell=True).decode('utf-8')
		for line in output.split('\n'):
			line = line.split()
			if len(line) > 0 and line[1] in function_names:
				data['Function Name'].append(line[1])
				data['Total Memory'].append(line[5])
				data['Total Memory %'].append(line[7])
				data['Own Memory'].append(line[9])
				data['Own Memory %'].append(line[11])
				data['Allocation Count'].append(line[13])
		# turn the data into a DataFrame and export as PNG
		df = pd.DataFrame(data)
		dfi.export(df, 'mem-profile-table.png', 
			table_conversion='matplotlib')
		os.remove("mem_data.bin")	
