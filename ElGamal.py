# -*- coding: utf-8 -*-

import argparse
import secrets
import pathlib
import mimetypes

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

    return r1, x1, y1


def find_inverse(a, p):

    """
        Returns inverse which is the element of the finite field.

        Args:
            a: integers for the equation ax + by = GCD(a, b)
            b: integers. prime number. the order of the finite field.
        Returns:
            inverse: integer x. Inverse of a such that ax = 1 (mod p)
            and inverse is the element of the finite field
    """

    remainder, inverse, y = extended_euclidean_algorithm(a, p)

    while 1:
        if inverse > 0:
            inverse = inverse % p
            return inverse
        else:
            inverse += p


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

    return secret_key


def write_secret_key(secret_key):
    with open('secret.key', 'w') as f:
        f.write("secret_key\n")
        f.write(str(secret_key))


def make_public_key(secret_key):
    """
        make public key and makes a file containing strings of
        these public keys

        Args:
            prime: integer. prime number
            secret_key: integer. secret key
     """
    prime = find_enough_big_prime_number()
    b = 0
    while b == 0:
        # b is preferably primitive element,but not necessary.
        b = secrets.randbelow(prime)
    y = pow(b, secret_key, prime)

    return y, b, prime


def write_public_key(y, b, prime):
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
    secret_key = make_secret_key()
    write_secret_key(secret_key)
    y, b, prime = make_public_key(secret_key)
    write_public_key(y, b, prime)


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


def get_message(message):

    """
        get message from file or string format and return it.

        Args:
            message: str or Path.file path to the cleartext or cleartext itself.

        Returns:
            message: str.cleartext
    """
    if not isinstance(message, str) and not isinstance(message, pathlib.Path):
        print("input str object or Path object.aborting...")
        exit()
    if isinstance(message, str):
        if message == "":
            print("message is empty.aborting...")
            exit()
        else:
            return message
    else:
        try:
            with message.open() as f:
                message = f.read()

            if message == "":
                print("message is empty.aborting...")
                exit()

            return message
        except UnicodeDecodeError:
            print("file is binary.aborting...")
            exit()


def ElGamal_encrypt(message, public_key_path, secret_key_path):
    """
        Encrypt a text with ElGamal cryptsystem.

        Args:
            message: string.we encrypt this string.
            random: integer.random number
            public_key_path: Path object. the path of a file
                             where the public key is stored.

        Returns:
            encrypted_message:Tuple (c1, c2), Encrypted message
    """
    y = 0
    b = 0
    prime = 0

    secret_key = 0

    while secret_key == 0:
        try:
            secret_key = read_secret_key(secret_key_path)
        except (FileNotFoundError, IsADirectoryError):
            print("secret key file not found. now generating...")
            secret_key = make_secret_key()
            write_secret_key(secret_key)

    while y == 0 and b == 0 and prime == 0:
        try:
            y, b, prime = read_public_key(public_key_path)
        except (FileNotFoundError, IsADirectoryError):
            print("public key file not found. now generating...")
            y, b, prime = make_public_key(secret_key)
            write_public_key(y, b, prime)

    message = get_message(message)
    message_integer = [ord(c) for c in message]

    random = secrets.randbelow(prime)
    c1 = pow(b, random, prime)
    c2_letters = [(pow(y, random, prime) * letter) % prime
                  for letter in message_integer]

    encrypted_message = (c1, c2_letters)

    return encrypted_message


def write_encrypted_message(encrypted_message):
    c1 = encrypted_message[0]
    c2_letters = encrypted_message[1]

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
             secret_key_path:integer. Path object of secret key.
        Returns:
             decrypted_message:string.Decrypted message.
    """
    try:
        y, b, prime = read_public_key(public_key_path)
    except (FileNotFoundError, IsADirectoryError):
        print("public key not found.aborting...")
        exit()

    try:
        secret_key = read_secret_key(secret_key_path)
    except (FileNotFoundError, IsADirectoryError):
        print("secret key not found,aborting...")
        exit()

    c2_list = []
    c1 = encrypted_message[0]
    for i in range(len(encrypted_message[1])):
        c2_list.append(encrypted_message[1][i])
    c1_x_power = pow(c1, secret_key, prime)
    c1_inverse = find_inverse(c1_x_power, prime)
    
    decrypted_message = ""
    for c2 in c2_list:
        decrypted_number = (c1_inverse * c2) % prime
        letter = chr(decrypted_number)
        decrypted_message += letter

    return decrypted_message


def write_decrypted_message(decrypted_message):
    with open('decrypted_message', 'w') as f:
        for letter in decrypted_message:
            f.write(letter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--encrypt", metavar="message",
                        help="encrypt a message")
    parser.add_argument("-d", "--decrypt", metavar="encrypted_message",
                        help="decrypt a encrypted_message")
    parser.add_argument("-p", "--public", help="specify public key file path",
                        action="store_true")
    parser.add_argument("-s", "--secret", help="specify secret key file path",
                        action="store_true")
    parser.add_argument("-m", "--make_keys",
                        help="make public keys and secret key files",
                        action="store_true")
    args = parser.parse_args()

    public_key_path = pathlib.Path()
    secret_key_path = pathlib.Path()

    if args.make_keys is True:
        make_key()
        print("We made the public key and the secret key")
        exit()
    if args.public is not None and args.public is True:
        public_key_path = pathlib.Path(args.public)
    if args.secret is not None and args.secret is True:
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
        encrypted_message = ElGamal_encrypt(encrypting_message_path,
                                            public_key_path)
        write_encrypted_message(encrypted_message)
    if args.decrypt is not None:
        decrypting_message_path = pathlib.Path(args.decrypt)
        decrypted_message = ElGamal_decrypt(decrypting_message_path,
                                            public_key_path, secret_key_path)
        write_decrypted_message(decrypted_message)

    parser.print_help()
