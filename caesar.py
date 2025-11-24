def caesar_encrypt(text, shift):
    result = ""
    for ch in text:
        if 'a' <= ch <= 'z':
            result += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
        elif 'A' <= ch <= 'Z':
            result += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += ch
    return result


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# ---------------- USER INPUTS ----------------

text = input("Enter text: ")
shift = int(input("Enter shift value (1–25): "))

print("\n1. Encrypt")
print("2. Decrypt")
choice = input("Choose option (1/2): ")

if choice == "1":
    encrypted = caesar_encrypt(text, shift)
    print("\nEncrypted Text:", encrypted)

elif choice == "2":
    decrypted = caesar_decrypt(text, shift)
    print("\nDecrypted Text:", decrypted)

else:
    print("Invalid option!")




#     #Theory

# A substitution cipher where each letter is shifted by a fixed number (e.g., +3).

# Example: A → D, B → E, … Z → C.

# Key = shift value (0–25).

# Total keys = 25 → very small.

# Advantages

# Very simple to implement.

# Fast and lightweight.

# Good for teaching basic cryptographic ideas.

# Disadvantages

# Only 25 keys → extremely easy to brute force.

# Frequency of letters is preserved → cryptanalysis is trivial.

# Not secure at all by modern standards.//