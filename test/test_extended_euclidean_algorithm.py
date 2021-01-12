# -*- coding: utf-8 -*-

import unittest
from ElGamal import extended_euclidean_algorithm


class TestExtendedEuclideanAlgorithm(unittest.TestCase):

    def test_extended_euclidean_algorithm(self):
        a = extended_euclidean_algorithm(100, 7)
        self.assertEqual(a, 4)

if __name__ == "__main__":
    unittest.main()
