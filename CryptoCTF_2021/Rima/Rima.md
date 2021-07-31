# Rima
### Sequences are known to be good solutions, but are they good problems?

Extracting the attached archive results in 3 files :
* [g.enc](./g.enc)
* [h.enc](./h.enc)
* [rima.py](./rima.py)
```python
	#!/usr/bin/env python
	from Crypto.Util.number import *
	from flag import FLAG

	def nextPrime(n):
	    while True:
	        n += (n % 2) + 1
	        if isPrime(n):
	            return n

	f = [int(x) for x in bin(int(FLAG.hex(), 16))[2:]]

	f.insert(0, 0)
	for i in range(len(f)-1): f[i] += f[i+1]

	a = nextPrime(len(f))
	b = nextPrime(a)

	g, h = [[_ for i in range(x) for _ in f] for x in [a, b]]

	c = nextPrime(len(f) >> 2)

	for _ in [g, h]:
	    for __ in range(c): _.insert(0, 0)
	    for i in range(len(_) -  c): _[i] += _[i+c]

	g, h = [int(''.join([str(_) for _ in __]), 5) for __ in [g, h]]

	for _ in [g, h]:
	    if _ == g:
	        fname = 'g'
	    else:
	        fname = 'h'
	    of = open(f'{fname}.enc', 'wb')
	    of.write(long_to_bytes(_))
	    of.close()
```

This script ciphers the flag into two files after a number of operations.
First, it gets the bitarray 'f' of the flag, adds each bit to the following one and generates 3 primes : a, b and c.

Then two lists g and h are respectively assigned to a times and b times the f list. The scrit then prepends 'c' 0 values and adds each value to the one located c indexes further.

Finally, g and h are used as base 5 integers, converted to base 10 integers and used as bytes for g.enc and h.enc

To decrypt the flag, we only need to do the same operations in the reverse order (cf [solve.py](./solve.py))
```python
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
```
