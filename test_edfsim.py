#!/usr/bin/env python

import unittest
from edfsim import *

class TestTaskPool(unittest.TestCase):

    def setUp(self):
        """Set up tests of the TaskPool."""
        self.tp = TaskPool()
        self.test_dict = {1: 'apple',
                          2: [1, 2, 3, 4],
                          'cat': 75,
                          'ringo': ['is', 'a', 'fat', 8008]}


    def test_TaskPool_known_key(self):
        """Ensure TaskPool objects behave like a normal dict when setting/accessing
        known key/value pairs.

        """
        for key, value in self.test_dict.items():
            self.tp[key] = value
            self.assertEqual(self.tp[key], value)


    def test_TaskPool_unknown_key(self):
        """Ensure TaskPool objects return an empty TaskQueue (currently an empty list)
        when setting/accessing unknown key/value pairs.

        """
        for key, value in self.test_dict.items():
            self.assertEqual([], self.tp[key])


class TestEDF(unittest.TestCase):

    def setUp(self):
        self.edf = EDF()


    def test_add_job(self):
        pass


    def test_remove_task(self):
        pass


    def test_pop_task(self):
        pass



if __name__ == '__main__':
    unittest.main()
