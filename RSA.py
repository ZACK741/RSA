# -*- coding: utf-8 -*-
from random import randrange, getrandbits
from fractions import Fraction
import sys

class RSA():
    def __init__(self, bitz):
        self.publicKey = None
        self.privateKey = None
        self.bitz = bitz

    def generate_key(self):
        print("find p")
        p = self.generate_prime_number()
        print("find q")
        q = self.generate_prime_number()
        while p == q:
            q = self.generate_prime_number()
        print("find n")
        n = p*q
        phi = (p-1)*(q-1)
        print("find e")
        e = self.generate_prime_number()
        while not self.co_prime(e, phi):
            e = self.generate_prime_number()
        print("find d now")
        sys.setrecursionlimit(3000)
        while(True):
            try:
                d = self.modinv(e, phi)
                break
            except Exception as msg:
                print(msg)
                print("remake e")
                e = self.generate_prime_number()
                while not self.co_prime(e, phi):
                    e = self.generate_prime_number()

        f = open("publicKey.txt", "a")
        f.write(str(e)+","+str(n))
        f.close()

        f = open("privateKey.txt", "a")
        f.write(str(d)+","+str(n))
        f.close()

    def is_prime(self, n, k=128):
        if n == 2 or n == 3:
            return True
        if n <= 1 or n % 2 == 0:
            return False
        # find r and s
        s = 0
        r = n - 1
        while r & 1 == 0:
            s += 1
            r //= 2
        # do k tests
        for _ in range(k):
            a = randrange(2, n - 1)
            x = pow(a, r, n)
            if x != 1 and x != n - 1:
                j = 1
                while j < s and x != n - 1:
                    x = pow(x, 2, n)
                    if x == 1:
                        return False
                    j += 1
                if x != n - 1:
                    return False
        return True

    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = self.egcd(b % a, a)
        return (g, x - (b // a) * y, y)


    def modinv(self, a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('No modular inverse')
        return x % m

    def generate_prime_candidate(self,length):
        p = getrandbits(length)
        # apply a mask to set MSB and LSB to 1
        p |= (1 << length - 1) | 1
        return p

    def generate_prime_number(self):
        p = 4
        # keep generating while the primality test fail
        while not self.is_prime(p, 128):
            p = self.generate_prime_candidate(self.bitz)
        return p

    def co_prime(self, a, b):
        if b % a == 0:
            return False
        f = Fraction(a, b)
        return f.numerator == a and f.denominator == b

    def encode(self):
        originalMessage = input("Enter: ")
        newStr = ""
        for m in originalMessage:
            m = str(ord(m))
            while len(m) != 3 :
                m = '0'+ m
            newStr += m
        asciiStr = int(newStr)
        try:
            with open('./publicKey.txt', 'r') as file:
                e, n = file.read().split(',')
            print(pow(asciiStr, int(e), int(n)))
        except Exception:
            print("no keys")
        input()

    def decode(self):
        msg = input("Enter: ")
        try:
            with open('./privateKey.txt', 'r') as file:
                d, n = file.read().split(',')
            m = str(pow(int(msg), int(d), int(n)))
            if len(m) % 3 != 0:
                m = "0" + m
            newStr = ""
            while m:
                c = m[:3]
                while c[0] == "0":
                    c = c[1:]
                newStr += chr(int(c))
                try:
                    m = m[3:]
                except IndexError:
                    break
            print(newStr)
        except Exception:
            print("no keys")
        input()


if __name__ == "__main__":
    r = RSA(2048)
    r.generate_key()




