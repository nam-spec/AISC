# -----------------------------------------
# Rail Fence Cipher - Encryption
# -----------------------------------------
def rail_fence_encrypt(text, rails):
    if rails <= 1:
        return text

    # Create rails (list of empty strings)
    fence = [''] * rails

    # Zig-zag variables
    row = 0
    direction = 1  # 1 = down, -1 = up

    # Place characters in zig-zag
    for ch in text:
        fence[row] += ch

        # Change direction at the top/bottom rail
        if row == rails - 1:
            direction = -1
        elif row == 0:
            direction = 1

        row += direction

    # Join all rails to form ciphertext
    return ''.join(fence)


# -----------------------------------------
# Rail Fence Cipher - Decryption
# -----------------------------------------
def rail_fence_decrypt(cipher, rails):
    if rails <= 1:
        return cipher

    # First, determine the zig-zag pattern positions
    pattern = [[] for _ in range(rails)]
    row = 0
    direction = 1

    # Mark positions with placeholders
    for i in range(len(cipher)):
        pattern[row].append(i)

        if row == rails - 1:
            direction = -1
        elif row == 0:
            direction = 1

        row += direction

    # Flatten pattern order to know fill sequence
    index_order = [idx for rail in pattern for idx in rail]

    # Create a list to place characters
    result = [''] * len(cipher)

    # Fill characters into the correct zig-zag positions
    for ci, pos in zip(cipher, index_order):
        result[pos] = ci

    # Return plaintext by joining
    return ''.join(result)


# -----------------------------------------
# Driver Code
# -----------------------------------------
if __name__ == "__main__":
    text = input("Enter text: ")
    rails = int(input("Enter number of rails: "))

    print("\n1. Encrypt\n2. Decrypt")
    choice = input("Choose option (1/2): ")

    if choice == '1':
        encrypted = rail_fence_encrypt(text, rails)
        print("\nEncrypted Text:", encrypted)

    elif choice == '2':
        decrypted = rail_fence_decrypt(text, rails)
        print("\nDecrypted Text:", decrypted)

    else:
        print("Invalid choice!")




# ✅ 6. Rail Fence Cipher
# Theory

# A transposition cipher.

# Write plaintext in zig-zag across rows (“rails”), then read row-wise.

# Example with 3 rails:

# H . . . O . . . R
# . E . L . W . L .
# . . L . . O . . D

# Advantages

# Simple and fast.

# No substitution → avoids frequency patterns.

# Disadvantages

# Very weak; easy to break using pattern analysis.

# Only changes positions, not letters.