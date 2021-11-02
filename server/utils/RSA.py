import math
import random


class RSA:
    def __init__(self, max_bit_size=8):
        self.__p, self.__q = self.__get_p_q(max_bit_size)

    def __get_prime(self, max_bit_size=8):
        max_num = 2 ** max_bit_size
        min_num = 2 ** (max_bit_size - 1)

        num = random.randint(min_num, max_num)

        if num < 1:
            return self.__get_prime(max_bit_size)
        else:
            for i in range(2, int(math.sqrt(num)) + 1):
                if (num % i) == 0:
                    return self.__get_prime(max_bit_size)
            return num

    def __get_p_q(self, max_bit_size=8):
        p = self.__get_prime(max_bit_size)
        q = self.__get_prime(max_bit_size)

        while p == q:
            q = self.__get_prime(max_bit_size)

        return p, q

    @staticmethod
    def __gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def __get_e(self, n, phi):
        e = random.randrange(1, phi)
        if self.__gcd(e, phi) != 1:
            return self.__get_e(n, phi)
        return e

    @staticmethod
    def __multiplicative_inverse(e, r):
        for i in range(r):
            if (e * i) % r == 1:
                return i

    def generate_keys(self):
        n = self.__p * self.__q
        phi = (self.__p - 1) * (self.__q - 1)

        e = self.__get_e(n, phi)
        d = self.__multiplicative_inverse(e, phi)
        return (e, n), (d, n)


def encrypt(text: str, key: tuple):
    e, n = key
    encrypted = [(ord(char) ** e) % n for char in text]
    return encrypted


def decrypt(encrypted_text: list, key: tuple):
    d, n = key
    decrypted_numbers = [chr((num ** d) % n) for num in encrypted_text]
    decrypted = ''.join(decrypted_numbers)
    return decrypted
