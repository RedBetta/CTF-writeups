#!/usr/bin/env python3

from Crypto.Util.number import *
# from flag import FLAG

def nextPrime(n):
    while True:
        n += (n % 2) + 1
        if isPrime(n):
            return n

FLAG = b"flag"
print("Flag =", FLAG)
f = [int(x) for x in bin(int(FLAG.hex(), 16))[2:]] # bitarray du flag
print("F =", f)

f.insert(0, 0)
print("F insert =", f)
for i in range(len(f)-1): f[i] += f[i+1]
print("F moving =", f)
print(len(f))
a = nextPrime(len(f))
b = nextPrime(a)

print("Prime A =", a)
print("Prime B =", b)

g = []
for x in [a]:
    for i in range(x): # 37
        for _ in f: # on ajoute 37 fois f à G
            g.append(_)
h = []
for x in [b]:
    for i in range(x): # 41
        for _ in f: # on ajoute 41 fois f à H
            h.append(_)

# print("G =", g)
# print("H =", h)

print(len(g), len(f), len(f)*a)
print(len(h), len(f), len(f)*b)

c = nextPrime(len(f) >> 2)
print("Prime C =", c)

# for _ in [g, h]:
#     for __ in range(c): _.insert(0, 0)
#     for i in range(len(_) -  c): _[i] += _[i+c]



#g
for i in range(c):
    g.insert(0, 0) # on insert c 0 au début de g
for i in range(len(g)-c):
    g[i] += g[i+c]

# print("NEW G =", g)


# #h
for i in range(c):
    h.insert(0, 0) # on insert c 0 au début de g
for i in range(len(h)-c):
    h[i] += h[i+c]

# print("NEW H =", h)

# g, h = [int(''.join([str(_) for _ in __]), 5) for __ in [g, h]]


#g

g5 = []
for e in g:
    g5.append(str(e))
g5 = int(''.join(g5), 5)
g = g5

print("G en base 5 =", g)


#h

h5 = []
for e in h:
    h5.append(str(e))
h5 = int(''.join(h5), 5)
h = h5
print("H en base 5 =", h)

for _ in [g, h]:
    if _ == g:
        fname = 'test_g'
    else:
        fname = 'test_h'
    of = open(f'{fname}.enc', 'wb')
    of.write(long_to_bytes(_))
    of.close()

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



# flag = decrypt("test_g.enc", "test_h.enc")

flag = decrypt("g.enc", "h.enc")
print("Flag =", flag)

# CCTF{_how_finD_7h1s_1z_s3cr3T?!}