import numpy as np

def char_to_num(c):
    return ord(c) - ord('A')

def num_to_char(n):
    return chr(n + ord('A'))

def get_key_matrix(n):
    print(f"Enter {n*n} numbers for the key matrix (row-wise):")
    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    return np.array(matrix)

def mod_inverse_matrix(matrix, mod=26):
    det = int(round(np.linalg.det(matrix))) % mod

    # Find inverse of determinant mod 26
    det_inv = None
    for i in range(mod):
        if (det * i) % mod == 1:
            det_inv = i
            break
    if det_inv is None:
        return None

    adj = np.round(det * np.linalg.inv(matrix)).astype(int) % mod
    return (det_inv * adj) % mod

def prepare_text(text, n):
    text = ''.join([c for c in text.upper() if c.isalpha()])
    while len(text) % n != 0:
        text += 'X'
    return text

def encrypt(text, key):
    n = key.shape[0]
    text = prepare_text(text, n)
    result = ""

    for i in range(0, len(text), n):
        block = np.array([char_to_num(c) for c in text[i:i+n]])
        enc = key.dot(block) % 26
        result += ''.join(num_to_char(x) for x in enc)

    return result

def decrypt(cipher, key):
    n = key.shape[0]
    inv_key = mod_inverse_matrix(key, 26)

    if inv_key is None:
        print("Key matrix has no modular inverse!")
        return ""

    result = ""
    for i in range(0, len(cipher), n):
        block = np.array([char_to_num(c) for c in cipher[i:i+n]])
        dec = inv_key.dot(block) % 26
        result += ''.join(num_to_char(x) for x in dec)

    return result


# ---------------- MAIN ----------------

text = input("Enter text: ")
n = int(input("Enter matrix size (e.g., 2 or 3): "))

key = get_key_matrix(n)

print("\n1. Encrypt")
print("2. Decrypt")
choice = input("Choice: ")

if choice == "1":
    print("\nEncrypted:", encrypt(text, key))
elif choice == "2":
    print("\nDecrypted:", decrypt(text, key))
else:
    print("Invalid option")


    

#     ✅ 5. Hill Cipher
# Theory

# Uses n×n matrix as a key.

# Plaintext is converted into numeric vectors.

# Ciphertext = Matrix × Vector (mod 26).

# Requires invertible key matrix.

# Advantages

# Strong diffusion: changes entire block, not letter-by-letter.

# Resistant to simple frequency attacks.

# Can encrypt blocks of size > 1.

# Disadvantages

# Susceptible to known plaintext attack (matrix can be solved).

# Requires matrix inverses mod 26 — easy to make mistakes.

# Not secure for real applications.