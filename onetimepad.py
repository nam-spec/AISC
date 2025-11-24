import os
import binascii

def otp_encrypt(plaintext: str):
    pt_bytes = plaintext.encode()

    # Generate random key equal to plaintext length
    key = os.urandom(len(pt_bytes))

    # XOR plaintext with key
    ciphertext = bytes([pt_bytes[i] ^ key[i] for i in range(len(pt_bytes))])

    return ciphertext, key


def otp_decrypt(ciphertext: bytes, key: bytes):
    plaintext = bytes([ciphertext[i] ^ key[i] for i in range(len(ciphertext))])
    return plaintext.decode()


# ------------------------------
# MAIN PROGRAM
# ------------------------------

plaintext = input("Enter the message to encrypt: ")

cipher, key = otp_encrypt(plaintext)

# Print key and cipher in hex format for readability
print("\n--- OTP Encryption Output ---")
print("Key (hex):", binascii.hexlify(key).decode())
print("Ciphertext (hex):", binascii.hexlify(cipher).decode())

# Optional: Demonstrate decryption
decrypted = otp_decrypt(cipher, key)
print("Decrypted message:", decrypted)



# Theory

# Key = truly random string of same length as plaintext.

# Encryption: 
# 𝐶
# =
# 𝑃
# ⊕
# 𝐾
# C=P⊕K

# Decryption: 
# 𝑃
# =
# 𝐶
# ⊕
# 𝐾
# P=C⊕K

# If key is random, used only once, kept fully secret, OTP is mathematically unbreakable.

# Advantages

# Perfect secrecy (proven by Shannon).

# No pattern, no frequency leakage.

# Unbreakable even with infinite computation.

# Disadvantages

# Key distribution problem — key must be as long as message.

# Must be used only once, else broken immediately.

# Difficult to store and manage large keys.

# Not practical for most real-world situations.