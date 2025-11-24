# convert character to 0–25
def char_to_num(c):
    return ord(c) - ord('a')

# convert 0–25 to char
def num_to_char(n):
    return chr(n + ord('a'))

# extend key to match text length
def extend_key(key, length):
    key = key.lower()
    clean = [c for c in key if c.isalpha()]
    out = ""
    i = 0
    while len(out) < length:
        out += clean[i % len(clean)]
        i += 1
    return out

# encrypt
def encrypt(text, key):
    text = text.lower()
    clean = [c for c in text if c.isalpha()]
    ext = extend_key(key, len(clean))
    out = ""
    for p, k in zip(clean, ext):
        c = (char_to_num(p) + char_to_num(k)) % 26
        out += num_to_char(c)
    return out

# decrypt
def decrypt(cipher, key):
    cipher = cipher.lower()
    clean = [c for c in cipher if c.isalpha()]
    ext = extend_key(key, len(clean))
    out = ""
    for c, k in zip(clean, ext):
        p = (char_to_num(c) - char_to_num(k)) % 26
        out += num_to_char(p)
    return out

# main workflow: input once, output both
key = input("Enter Vernam key: ").strip()
text = input("Enter text: ")

enc = encrypt(text, key)
dec = decrypt(enc, key)

print("Encrypted:", enc)
print("Decrypted:", dec)



# ✅ 3. Polyalphabetic Cipher (e.g., Vigenère)
# Theory

# Uses multiple substitution alphabets → letters change depending on key position.

# Vigenère uses a repeating keyword (e.g., “SECRET”).

# Reduces direct frequency mapping.

# Advantages

# Stronger than monoalphabetic.

# Not vulnerable to single-letter frequency analysis.

# More confusion + better distribution of ciphertext.

# Disadvantages

# If key is short → periodicity → can be broken using Kasiski test or Friedman test.

# Still not secure for modern use.

# Repeated key patterns leak structure.