

import unittest
from ElGamal import is_prime


class TestIsprime(unittest.TestCase):


    def test_is_prime(self):
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(2))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(13434324234))
        self.assertTrue(is_prime(9923))
        self.assertFalse(is_prime(9925))
