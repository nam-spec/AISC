def generate_key_matrix(key) :
    key = key.upper().replace("J", "I")
    matrix = []
    used = set()

    for char in key : 
        if char not in used and char.isalpha():
            matrix.append(char)
            used.add(char)

    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in used : 
            used.add(char)
            matrix.append(char)

    matrix = [matrix[i : i+5] for i in range(0, 25, 5)]
    return matrix

def find_position(matrix, key):    
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == key:
                return i,j
    return None

def prepare_text(text) :
    text = text.upper().replace("J", "I")
    clean = ""

    for char in text :
        if char.isalpha():
            clean += char
    
    digraphs = []
    i = 0
    while i < len(clean):
        a = clean[i]
        if i + 1 < len(clean):
            b = clean[i + 1]
            if a == b :
                digraphs.append(a + "X")
                i += 1
            else:
                digraphs.append(a + b)
                i += 2
        else:
            digraphs.append(a + "X")
            i += 1

    return digraphs
    
def encrpyt_digraph(di, matrix):
    a , b = di[0], di[1]
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    if r1 == r2 : 
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    if c1 == c2:
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    
    return matrix[r1][c2] + matrix[r2][c1]

def decrpyt_digraph(di, matrix):
    a , b = di[0], di[1]
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    if r1 == r2 : 
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    if c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    
    return matrix[r1][c2] + matrix[r2][c1]

def encrpyt(pt, key):
    matrix = generate_key_matrix(key) 
    print(matrix)
    digraphs = prepare_text(pt)
    ct = ""
    for di in digraphs :
        ct += encrpyt_digraph(di, matrix)

    return ct

def decrypt(ct, key):
    matrix = generate_key_matrix(key) 
    digraphs = prepare_text(ct)
    pt = ""
    for di in digraphs :
        pt += decrpyt_digraph(di, matrix)

    return pt

key = input("enter the key : ")

print("1. encrpyt")
print("2. decrpyt")

while(True) :
    choice = input("Enter the choice : ")
    if choice =="1":
        pt = input("enter plaintext : ")
        print(encrpyt(pt, key))
    if choice == "2" :
        ct = input("enter the ciphertext : ")
        print(decrypt(ct, key))



#         ✅ 4. Playfair Cipher
# Theory

# Uses a 5×5 matrix of letters generated from a keyword.

# Encrypts digraphs (pairs of letters).

# Rules: same-row → shift right, same-column → shift down, rectangle → swap corners.

# Advantages

# Harder than monoalphabetic (ciphertext is based on pairs, not single letters).

# Frequency of single letters is obscured.

# Resistant to simple frequency analysis.

# Disadvantages

# Still vulnerable to digraph frequency analysis.

# Key must be shared secretly.

# Not strong enough for modern cryptography.