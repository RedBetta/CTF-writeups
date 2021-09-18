from pwn import *

def send(r, hex_message):
	r.sendline(hex_message)
	r.recv()
	return r.recv().decode().split('\n')[1].replace("Le ciphertext: ", '')

r = remote("157.159.191.52" ,25007)
print(r.recv())
flag = b"HackademINT{".hex()

l = 92 # length of the ciphertext

while b'}' not in bytes.fromhex(flag):
	for i in range(128):
		y = hex(i)[2:].zfill(2)
		ciphertext = send(r, flag + y)
		# print(ciphertext)
		if len(ciphertext) == 92:
			flag += y
			print("Found letter :", y, bytes.fromhex(y))
			break
	print("Current flag =", bytes.fromhex(flag))
print("Flag =", bytes.fromhex(flag))