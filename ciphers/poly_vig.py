# convert character to number 0-25
def char_to_num(c):
    return ord(c) - ord('a')

# convert number 0-25 to character
def num_to_char(n):
    return chr(n + ord('a'))

# generate repeated key matching text length
def extend_key(key, length):
    key = key.lower()
    key_clean = [c for c in key if c.isalpha()]
    repeated = ""
    i = 0
    while len(repeated) < length:
        repeated += key_clean[i % len(key_clean)]
        i += 1
    return repeated

# encrypt plaintext
def encrypt(text, key):
    text = text.lower()
    clean = [c for c in text if c.isalpha()]
    ext_key = extend_key(key, len(clean))
    out = ""
    for t, k in zip(clean, ext_key):
        ct = (char_to_num(t) + char_to_num(k)) % 26
        out += num_to_char(ct)
    return out

# decrypt ciphertext
def decrypt(cipher, key):
    cipher = cipher.lower()
    clean = [c for c in cipher if c.isalpha()]
    ext_key = extend_key(key, len(clean))
    out = ""
    for c, k in zip(clean, ext_key):
        pt = (char_to_num(c) - char_to_num(k)) % 26
        out += num_to_char(pt)
    return out

# main
key = input("Enter key: ").strip()

while True:
    print("\n--- Polyalphabetic (Vigenère) Cipher ---")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")

    ch = input("Enter choice: ").strip()

    if ch == "1":
        txt = input("Enter text to encrypt: ")
        print("Encrypted:", encrypt(txt, key))

    elif ch == "2":
        txt = input("Enter text to decrypt: ")
        print("Decrypted:", decrypt(txt, key))

    elif ch == "3":
        break

    else:
        print("Invalid choice.")