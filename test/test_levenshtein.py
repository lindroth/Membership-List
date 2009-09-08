#! /usr/bin/python
# This Python file uses the following encoding: utf-8
import sys
sys.path.append('../lib')
import levenshtein
import unittest

class TestLevenshtein(unittest.TestCase):
  def test_algorith(self):
    """Test the algorithm for some strings"""
    name = "abba"
    word_list = [ "abba", "acba", "abbba", "ackbar" ]
    answer_list = [0, 1, 1, 3]
    index = 0
    for word in word_list:
      self.assertEqual(answer_list[index],levenshtein.levenshtein(name, word))
      index += 1

if __name__ == '__main__':
  unittest.main()
