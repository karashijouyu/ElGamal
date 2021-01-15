

import unittest
from ElGamal import is_prime
from ElGamal import find_enough_big_prime_number


class TestFindEnoughBigPrimeNumber(unittest.TestCase):

    def test_enough_big_prime(self):
        prime = find_enough_big_prime_number()
        self.assertTrue(is_prime(prime))
