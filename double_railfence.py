import math

# -----------------------------------------------------
# SINGLE ROW–COLUMN ENCRYPTION
# -----------------------------------------------------
def row_column_encrypt(text, rows):
    text = text.replace(" ", "")
    n = len(text)
    cols = math.ceil(n / rows)

    # Build matrix row-wise
    matrix = []
    index = 0
    for r in range(rows):
        row = []
        for c in range(cols):
            if index < n:
                row.append(text[index])
                index += 1
            else:
                row.append(None)
        matrix.append(row)

    # Read column-wise → ciphertext
    cipher = ""
    for c in range(cols):
        for r in range(rows):
            if matrix[r][c] is not None:
                cipher += matrix[r][c]

    return cipher


# -----------------------------------------------------
# SINGLE ROW–COLUMN DECRYPTION
# -----------------------------------------------------
def row_column_decrypt(cipher, rows):
    cipher = cipher.replace(" ", "")
    n = len(cipher)
    cols = math.ceil(n / rows)

    # How many characters per row?
    full_rows = n // cols
    last_row_len = n % cols

    # Build matrix with exact row sizes
    matrix = []
    for r in range(rows):
        if r < full_rows:
            matrix.append([None] * cols)
        elif r == full_rows and last_row_len != 0:
            matrix.append([None] * last_row_len)
        else:
            matrix.append([])

    # Fill column-wise from ciphertext
    index = 0
    for c in range(cols):
        for r in range(rows):
            if c < len(matrix[r]):
                matrix[r][c] = cipher[index]
                index += 1

    # Read row-wise → plaintext
    plain = ""
    for r in range(rows):
        for c in range(len(matrix[r])):
            plain += matrix[r][c]

    return plain


# -----------------------------------------------------
# DOUBLE ENCRYPTION
# -----------------------------------------------------
def double_row_column_encrypt(text, rows):
    cipher1 = row_column_encrypt(text, rows)
    cipher2 = row_column_encrypt(cipher1, rows)
    return cipher2


# -----------------------------------------------------
# DOUBLE DECRYPTION
# -----------------------------------------------------
def double_row_column_decrypt(cipher, rows):
    plain1 = row_column_decrypt(cipher, rows)
    plain2 = row_column_decrypt(plain1, rows)
    return plain2


# -----------------------------------------------------
# DRIVER CODE
# -----------------------------------------------------
text = input("Enter plaintext: ")
rows = int(input("Enter number of rows: "))

cipher = double_row_column_encrypt(text, rows)
plain = double_row_column_decrypt(cipher, rows)

print("\nDouble Encryption Ciphertext:", cipher)
print("Decrypted Text:", plain)


# ✅ 8. Double Row-Column Rail Fence (Double Transposition)
# Theory

# Apply row-column transposition twice using two different keys.

# Strongest classical transposition cipher.

# Advantages

# Much stronger than simple transposition.

# Harder to break without computational search.

# Widely used historically (e.g., WW1/WW2).

# Disadvantages

# Still not secure vs modern computers.

# Complex to encrypt/decrypt manually.

# Requires keeping 2 keys secret.. #