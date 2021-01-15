# -*- coding: utf-8 -*-

import unittest
from ElGamal import extended_euclidean_algorithm


class TestExtendedEuclideanAlgorithm(unittest.TestCase):

    def identity_bool(self,r, a, b, x, y):
        identity = r == a * x + b * y
        return identity

    def test_extended_euclidean_algorithm(self):
        r, x, y = extended_euclidean_algorithm(3, 7)
        identity = r == 3*x + 7*y
        self.assertTrue(identity)

        r, x, y = extended_euclidean_algorithm(-29, 10)
        self.assertTrue(self.identity_bool(r, -29, 10, x, y))

        r, x, y = extended_euclidean_algorithm(13424723473247, 23523523)
        self.assertTrue(self.identity_bool(r, 13424723473247, 23523523, x, y))


if __name__ == "__main__":
    unittest.main()
