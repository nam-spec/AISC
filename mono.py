def validate_key(key):
    key = key.upper()
    if len(key) != 26:
        return False
    return len(set(key)) == 26  # all letters must be unique


def encrypt_mono(text, key):
    key = key.upper()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mapping = {alphabet[i]: key[i] for i in range(26)}

    result = ""
    for ch in text:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            mapped = mapping[ch.upper()]
            result += mapped if ch.isupper() else mapped.lower()
        else:
            result += ch

    return result


def decrypt_mono(text, key):
    key = key.upper()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    reverse_mapping = {key[i]: alphabet[i] for i in range(26)}

    result = ""
    for ch in text:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            mapped = reverse_mapping[ch.upper()]
            result += mapped if ch.isupper() else mapped.lower()
        else:
            result += ch

    return result


# --------------- USER INPUTS -----------------

text = input("Enter text: ")
key = input("Enter 26-letter key (e.g., QWERTYUIOPASDFGHJKLZXCVBNM): ")

if not validate_key(key):
    print("\nInvalid key! Key must contain exactly 26 unique letters.")
    exit()

print("\n1. Encrypt")
print("2. Decrypt")
choice = input("Choose option (1/2): ")

if choice == "1":
    encrypted = encrypt_mono(text, key)
    print("\nEncrypted Text:", encrypted)

elif choice == "2":
    decrypted = decrypt_mono(text, key)
    print("\nDecrypted Text:", decrypted)

else:
    print("Invalid option!")






# ✅ 2. Monoalphabetic Substitution Cipher
# Theory

# Each letter of plaintext maps to one unique letter of ciphertext.

# Key = a random permutation of the alphabet (26! possible).

# Example: A→Q, B→M, C→Z …

# Advantages

# Large keyspace (26!) compared to Caesar.

# Harder to brute force than Caesar.

# Disadvantages

# Still vulnerable to frequency analysis.

# Once some letters are discovered, entire plaintext leaks.

# Not secure for modern communication.