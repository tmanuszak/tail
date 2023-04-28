from collections import deque
import numpy as np

def check_bounds(sequence, n):
	if n == 0:
		return []
	elif n > len(sequence):
		raise IndexError
	return sequence	

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
