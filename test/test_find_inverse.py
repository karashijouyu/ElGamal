
import unittest
from ElGamal import extended_euclidean_algorithm
from ElGamal import find_inverse


class TestFindInverse(unittest.TestCase):

    def test_find_inverse(self):

        a = 3
        p = 7
        r, x, y = extended_euclidean_algorithm(a, p)
        x = find_inverse(a, p)
        # check if x is the element of the finite field
        self.assertGreater(x, 0)
        self.assertLess(x, p)
        # check if x is the inverse of a in modular p.
        modular = a * x % p
        self.assertEqual(1, modular)

        a = -29
        p = 10
        r, x, y = extended_euclidean_algorithm(a, p)
        x = find_inverse(a, p)
        self.assertGreater(x, 0)
        self.assertLess(x, p)
        modular = a * x % p
        self.assertEqual(1, modular)
