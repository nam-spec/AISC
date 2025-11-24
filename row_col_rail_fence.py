import math

# -----------------------------------------------------
# ROW–COLUMN RAIL FENCE ENCRYPTION
# -----------------------------------------------------
def row_column_encrypt(plaintext, rows):
    plaintext = plaintext.replace(" ", "")
    n = len(plaintext)

    cols = math.ceil(n / rows)

    # Build matrix row-wise
    matrix = []
    index = 0

    for r in range(rows):
        row = []
        for c in range(cols):
            if index < n:
                row.append(plaintext[index])
                index += 1
            else:
                row.append(None)
        matrix.append(row)

    # Read column-wise
    ciphertext = ""
    for c in range(cols):
        for r in range(rows):
            if matrix[r][c] is not None:
                ciphertext += matrix[r][c]

    return ciphertext


# -----------------------------------------------------
# ROW–COLUMN RAIL FENCE DECRYPTION
# -----------------------------------------------------
def row_column_decrypt(ciphertext, rows):
    ciphertext = ciphertext.replace(" ", "")
    n = len(ciphertext)

    cols = math.ceil(n / rows)

    # How many rows are FULL?
    full_rows = n // cols
    last_row_len = n % cols

    # Build matrix with correct row lengths
    matrix = []
    for r in range(rows):
        if r < full_rows:
            matrix.append([None] * cols)
        elif r == full_rows and last_row_len != 0:
            matrix.append([None] * last_row_len)
        else:
            matrix.append([])

    # Fill column-wise
    index = 0
    for c in range(cols):
        for r in range(rows):
            if c < len(matrix[r]):
                matrix[r][c] = ciphertext[index]
                index += 1

    # Read row-wise → plaintext
    plaintext = ""
    for r in range(rows):
        for c in range(len(matrix[r])):
            plaintext += matrix[r][c]

    return plaintext


# -----------------------------------------------------
# DRIVER CODE
# -----------------------------------------------------
text = input("Enter plaintext: ")
rows = int(input("Enter number of rows: "))

cipher = row_column_encrypt(text, rows)
plain = row_column_decrypt(cipher, rows)

print("\nCiphertext:", cipher)
print("Decrypted Text:", plain)



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