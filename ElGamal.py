# -*- coding: utf-8 -*-

import argparse
import secrets
import pathlib


def extended_euclidean_algorithm(a, b):
    """
    Find a in Z when equation ax+by = GCD(a, b).
        Args:
            a,b: integers such that ax+by = GCD(a, b).

        Returns:
            x1: integers such that a * x1 + b * y = GCD(a, b)
            for given a and b.
    """

    r1 = a
    x1 = 1
    y1 = 0

    r2 = b
    x2 = 0
    y2 = 1

    while r2 != 0:
        # r1 = qr2 + r3
        r3 = r1 % r2
        q = r1 // r2

        x3 = x1 - q * x2
        y3 = y1 - q * y2

        r1 = r2
        r2 = r3

        x1 = x2
        y1 = y2
        x2 = x3
        y2 = y3

    return x1


def is_prime(n):
    """
       Millar-Rabin primality test

        Args:
            n:integer. we check whether n is the prime number

        Returns:
            0 or 1:boolean value.
    """
    if n == 2:
        return 1
    if n == 1 or n & 1 == 0:
        return 0

    power_two_times_odd = n - 1
    index_of_two = 0

    while power_two_times_odd & 1 == 0:
        power_two_times_odd >>= 1
        index_of_two += 1

    odd_remained = power_two_times_odd

    a = 0
    while a < 2:
        a = secrets.randbelow(n)

    y = pow(a, odd_remained, n)
    for _ in range(20):
        if y == 1 or y == n - 1:
            return 1
        i = 0
        while 1:
            if y == n - 1:
                break
            if i == index_of_two:
                return 0
            y = pow(y, 2, n)
            i += 1
    return 1


def find_enough_big_prime_number():
    """
        I refered to this document for the size of key bits.
        https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final, 54p

        Returns:
            prime: integer. a prime number.
    """
    key_bits = 3072
    found = 0
    print("now finding prime number...")
    while found == 0:
        prime = secrets.randbits(key_bits)
        found = is_prime(prime)
    print("prime number found!")

    return prime


def make_secret_key():
    """
        find secret key
        I refered to this document for the size of key bits.
        https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final, 54p

        returns secret key:integer. secure secret key.
    """
    key_bits = 256

    secret_key = secrets.randbits(key_bits)

    with open('secret.key', 'w') as f:
        f.write("secret_key\n")
        f.write(str(secret_key))


def make_public_key(prime):
    """
        make public key and makes a file containing strings of
        these public keys

        Args:
            prime: integer. prime number
            secret_key: integer. secret key
    """
    while 1:
        try:
            with open('secret.key', 'r') as f:
                f.readline()
                secret_key = int(f.readline())
            break
        except FileNotFoundError:
            print("There's no secret key.making secret key...")
            make_secret_key()

    b = 0
    while b == 0:
        # b is preferably generating element,but not necessary.
        b = secrets.randbelow(prime)
    y = pow(b, secret_key, prime)
    with open('public.key', 'w') as f:
        f.write("y:\n")
        f.write(str(y))
        f.write("\n")
        f.write("b:\n")
        f.write(str(b))
        f.write("\n")
        f.write("prime number:\n")
        f.write(str(prime))


def make_key():
    prime = find_enough_big_prime_number()
    make_public_key(prime)


def read_public_key(public_key_path):
    with public_key_path.open() as f:
        f.readline()
        y = int(f.readline())
        f.readline()
        b = int(f.readline())
        f.readline()
        prime = int(f.readline())
    return y, b, prime


def read_secret_key(secret_key_path):
    with secret_key_path.open() as f:
        f.readline()
        secret_key = int(f.readline())

    return secret_key


def ElGamal_encrypt(message_path, public_key_path):
    """
        Encrypt a text with ElGamal cryptsystem.

        Args:
            message: string.we encrypt this string.
            random: integer.random number
            public_key_path: Path object. the path of a file
                             where the public key is stored.

        Returns:
            (c1, c2):Tuple, Encrypted message
    """
    y = 0
    b = 0
    prime = 0
    while y == 0 and b == 0 and prime == 0:
        try:
            with public_key_path.open() as f:
                f.readline()
                y = int(f.readline())
                f.readline()
                b = int(f.readline())
                f.readline()
                prime = int(f.readline())
        except FileNotFoundError:
            print("Keys not found."
                  "Please make public key and secret key first.")
            exit()
    with message_path.open() as f:
        message = f.read()

    message_integer = [ord(c) for c in message]

    random = secrets.randbelow(prime)
    c1 = pow(b, random, prime)
    c2_letters = [(pow(y, random, prime) * letter) % prime
                  for letter in message_integer]

    with open('encrypted_message', 'w') as f:
        f.write("c1:\n")
        f.write(str(c1))
        f.write("\n")
        f.write("c2:\n")
        for c2 in c2_letters:
            f.write(str(c2))
            f.write("\n")

 
def ElGamal_decrypt(encrypted_message, public_key_path, secret_key_path):
    """
        Decrypt a text with ElGamal cryptsystem.

        Args:
             encrypted_message:Tuple of integers. encrypted message
             public_key_path: Path object of public key.
             secret_key:integer. Path object of secret key.
        Returns:
            message:integer.Decrypted message.
    """
    y, b, prime = read_public_key(public_key_path)
    secret_key = read_secret_key(secret_key_path)

    c2_list = []
    with encrypted_message.open() as f:
        f.readline()
        c1 = int(f.readline())
        f.readline()
        c2 = int(f.readline())
        while c2 != '':
            c2_int = int(c2)
            c2_list.append(c2_int)
            c2 = f.readline()
    # Let p:prime. GCD(a,p) = 1 where 0 < a < p.
    # ax + bp = 1 (mod p) -> ax = 1 (mod p) so x is a's inverse in (mod p).
    c1_power_secret_key_inverse = \
        extended_euclidean_algorithm(pow(c1, secret_key, prime), prime)

    message_sequence = []
    for c2 in c2_list:
        letter = chr((c2 * c1_power_secret_key_inverse) % prime)
        message_sequence.append(letter)
    with open('decrypted_message', 'w') as f:
        for letter in message_sequence:
            f.write(letter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--encrypt", type=str)
    parser.add_argument("-d", "--decrypt", type=str)
    parser.add_argument("-p", "--public", type=str)
    parser.add_argument("-s", "--secret", type=str)
    parser.add_argument("-m", "--make_keys", action="store_true")
    args = parser.parse_args()

    public_key_path = pathlib.Path()
    secret_key_path = pathlib.Path()

    if args.make_keys is True:
        make_key()
        print("We made the public key and the secret key")
        exit()
    if args.public is not None:
        public_key_path = pathlib.Path(args.public)
    if args.secret is not None:
        secret_key_path = pathlib.Path(args.secret)

    if not public_key_path.exists() or not secret_key_path.exists():
        while 1:
            print("there's no key files!")
            print("Do you want to make them? y/n")
            yes_or_no = input()
            yes = ['y', 'yes', 'Yes', 'YES']
            no = ['n', 'no', 'No', 'NO']
            if yes_or_no in yes:
                make_key()
                break
            elif yes_or_no in no:
                print("aborting...")
                exit()
            else:
                print("Please type y or n")

    if args.encrypt is not None and args.decrypt is not None:
        print("You can't decrypt and encrypt text at the same time.")
        print("Choose only one of the -e or -d options")
        exit()

    if args.encrypt is not None:
        encrypting_message_path = pathlib.Path(args.encrypt)
        ElGamal_encrypt(encrypting_message_path, public_key_path)
    if args.decrypt is not None:
        decrypting_message_path = pathlib.Path(args.decrypt)
        ElGamal_decrypt(decrypting_message_path, public_key_path,
                        secret_key_path)
