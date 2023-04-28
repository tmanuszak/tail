import unittest
import tail
from collections import deque
import numpy as np

class TestTail(unittest.TestCase):
	def test_tail_slicing(self):
		l = list(range(10))
		answer = [7, 8, 9]
		self.assertEqual(tail.tail_slicing(l, 3), answer)
	
	def test_tail_appending(self):
		l = list(range(10))
		answer = [7, 8, 9]
		self.assertEqual(tail.tail_appending(l, 3), answer)
	
	def test_tail_list_comp(self):
		l = list(range(10))
		answer = [7, 8, 9]
		self.assertEqual(tail.tail_list_comp(l, 3), answer)
	
	def test_tail_deque(self):
		l = list(range(10))
		answer = deque([7, 8, 9])
		self.assertEqual(tail.tail_deque(l, 3), answer)
	
	def test_tail_return_generator(self):
		l = list(range(10))
		answer = [7, 8, 9]
		self.assertEqual(list(tail.tail_return_generator(l, 3)), answer)
	
	def test_tail_generator_plus_list(self):
		l = list(range(10))
		answer = [7, 8, 9]
		self.assertEqual(list(tail.tail_generator_plus_list(l, 3)), answer)
	
	def test_tail_numpy_slicing(self):
		l = np.array(list(range(10)))
		answer = np.array([7, 8, 9])
		self.assertEqual(tail.tail_numpy_slicing(l, 3).all(), answer.all())
	

if __name__ == '__main__':
	unittest.main()
