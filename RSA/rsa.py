
import math

# Greatest Common Divisor
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Extended Euclidean Algorithm (mod inverse)
def mod_inverse(e, phi):
    old_r, r = e, phi
    old_s, s = 1, 0

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s

    return old_s % phi

# Key generation
def generate_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 2
    while e < phi:
        if gcd(e, phi) == 1:
            break
        e += 1

    d = mod_inverse(e, phi)
    return (e, n), (d, n)

# Encrypt
def encrypt(msg, public_key):
    e, n = public_key
    return [pow(ord(ch), e, n) for ch in msg]

# Decrypt
def decrypt(cipher, private_key):
    d, n = private_key
    return ''.join(chr(pow(c, d, n)) for c in cipher)


print("\n=== RSA Encryption / Decryption ===\n")

p = int(input("Enter prime p: "))
q = int(input("Enter prime q: "))

public_key, private_key = generate_keys(p, q)

print("\nPublic Key :", public_key)
print("Private Key:", private_key)

while True:
    print("\n1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")
    choice = input("Select option: ")

    if choice == "1":
        msg = input("Enter message: ")
        cipher = encrypt(msg, public_key)

        # Print space-separated for easy copy-paste
        print("Encrypted:", " ".join(str(x) for x in cipher))

    elif choice == "2":
        cipher = input("Enter cipher values (space-separated): ")
        cipher = list(map(int, cipher.split()))
        plain = decrypt(cipher, private_key)
        print("Decrypted Message:", plain)

    elif choice == "3":
        print("Exiting.")
        break

    else:
        print("Invalid choice, try again.")
