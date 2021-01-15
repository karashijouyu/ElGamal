

import unittest
from ElGamal import ElGamal_encrypt
from ElGamal import ElGamal_decrypt
from pathlib import Path


class TestEncryptionDecryption(unittest.TestCase):

    def test_encryption_to_decryption(self):

        message = "this is a test"

        public_key_path = Path("public.key")
        secret_key_path = Path("secret.key")
        encrypted = ElGamal_encrypt(message, public_key_path, secret_key_path)
        decrypted = ElGamal_decrypt(encrypted, public_key_path,
                                    secret_key_path)
        self.assertEqual(message, decrypted)
