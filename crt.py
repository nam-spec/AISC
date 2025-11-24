def modinv(a, m):
    r0, r1 = a, m
    s0, s1 = 1, 0
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if r0 != 1:
        raise ValueError(f"No inverse for {a} mod {m}")
    return s0 % m


def crt(a, m):
    M = 1
    for mi in m:
        M *= mi

    x = 0
    for ai, mi in zip(a, m):
        Mi = M // mi
        inv = modinv(Mi % mi, mi)
        x += ai * Mi * inv
    return x % M


# ------------------ User Input ------------------
k = int(input("Enter number of moduli: "))

moduli = []
print("Enter moduli (must be pairwise coprime):")
for _ in range(k):
    moduli.append(int(input()))

print("\nEnter X residues:")
x_res = []
for mi in moduli:
    x_res.append(int(input(f"x mod {mi} = ")))

print("\nEnter Y residues:")
y_res = []
for mi in moduli:
    y_res.append(int(input(f"y mod {mi} = ")))

# ------------------ Perform All Operations ------------------
results = {}

# Addition
add_res = [(x + y) % m for (x, y, m) in zip(x_res, y_res, moduli)]
results["x + y"] = crt(add_res, moduli)

# Subtraction
sub_res = [(x - y) % m for (x, y, m) in zip(x_res, y_res, moduli)]
results["x - y"] = crt(sub_res, moduli)

# Multiplication
mul_res = [(x * y) % m for (x, y, m) in zip(x_res, y_res, moduli)]
results["x * y"] = crt(mul_res, moduli)

# Division
inv_list = [modinv(y, m) for (y, m) in zip(y_res, moduli)]
div_res = [(x * inv) % m for (x, inv, m) in zip(x_res, inv_list, moduli)]
results["x / y"] = crt(div_res, moduli)

# ------------------ Output ------------------
mod_prod = 1
for m in moduli:
    mod_prod *= m

print("\n----- RESULTS -----")
print(f"Modulus product = {mod_prod}")

print("\nAddition:")
print("Residues =", add_res)
print("Result   =", results['x + y'])

print("\nSubtraction:")
print("Residues =", sub_res)
print("Result   =", results['x - y'])

print("\nMultiplication:")
print("Residues =", mul_res)
print("Result   =", results['x * y'])

print("\nDivision:")
print("Residues =", div_res)
print("Result   =", results['x / y'])