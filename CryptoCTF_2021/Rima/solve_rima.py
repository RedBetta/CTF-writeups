#!/usr/bin/env python3

from gmpy2 import digits

def get_file_in_base(filename, base):
    with open(filename, "rb") as f:
        return [int(e) for e in str(digits(bytes_to_long(f.read()), base))]

def previousPrime(n):
    while True:
        n -= (n % 2) + 1
        if isPrime(n):
            return n 

def get_prime_C(g, h):
    n = max(g[::-1].index(3), h[::-1].index(3))
    # Find closest prime <= n
    c = previousPrime(n)
    return c

def get_Fab(g, h, c):
    diff = h[len(g):]
    divisors = [i for i in range(2, len(diff)) if len(diff) % i == 0]
    for l in divisors:
        f = diff[0:l]
        for i in range(l, len(diff)-l, l):
            if diff[i:i+l] != f:
                continue
        a = len(g)//l
        b = len(h)//l
        if isPrime(a) and isPrime(b):
            return f, a, b

def decrypt(g_enc, h_enc):
    base = 5
    g, h = get_file_in_base(g_enc, base), get_file_in_base(h_enc, base)
    c = get_prime_C(g, h)
    print("Found c prime =", c)
    for x in [g, h]:
        for i in range(len(x)-c-1, 0, -1):
            x[i] -= x[i+c]
    g, h = g[c:], h[c:]
    print(g)
    f, a, b = get_Fab(g, h, c)
    print("Found primes A =", a, "and B =", b)
    for i in range(len(f)-2, 0, -1):
        f[i] -= f[i+1]
    f = f[1:]
    flag = long_to_bytes(int(''.join(str(b) for b in f), 2))
    return flag

flag = decrypt("g.enc", "h.enc")
print("Flag =", flag)

# CCTF{_how_finD_7h1s_1z_s3cr3T?!}