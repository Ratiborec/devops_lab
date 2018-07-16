import task25

from unittest import TestCase


class TestTask(TestCase):

  def setUp(self):
    """Init"""

  def test_sort_chars(self):
    self.assertEqual(task25.sort_chars({}), {})
    self.assertEqual(task25.sort_chars(1), "Incorrect data")
    self.assertEqual(task25.sort_chars({"a": 0}), {"a": 0})

  def test_output(self):
	  self.assertEqual(task25.sort_chars(1), "Incorrect data")
	  self.assertEqual(task25.sort_chars({}), {})
	  self.assertEqual(task25.sort_chars({"a": 0}), {"a": 0})

  def test_count_char(self):
	  self.assertEqual(task25.sort_chars(1), "Incorrect data")
	  self.assertEqual(task25.sort_chars([4, 3, 34, 4]), "Incorrect data")
	  self.assertEqual(task25.sort_chars({"a": 0}), {"a": 0})

  def tearDown(self):
    """Finish"""
