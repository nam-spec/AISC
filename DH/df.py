
import random

def diffie_hellman():
    print("=== Diffie-Hellman Key Exchange ===")

    p = int(input("Enter a large prime number (p): "))
    g = int(input("Enter a primitive root of p (g): "))

    print(f"\nPublic values: p = {p}, g = {g}")

    a = random.randint(2, p - 2)     
    b = random.randint(2, p - 2)    

    print(f"\nAlice private key (random): {a}")
    print(f"Bob private key (random):   {b}")

    # Public values exchanged
    A = pow(g, a, p)    # Alice sends this
    B = pow(g, b, p)    # Bob sends this

    print(f"\nAlice sends public value A = {A}")
    print(f"Bob sends public value B = {B}")

    # Shared secret computation
    secret_A = pow(B, a, p)
    secret_B = pow(A, b, p)

    print(f"\nAlice computes shared secret = {secret_A}")
    print(f"Bob computes shared secret = {secret_B}")

    # Check correctness
    if secret_A == secret_B:
        print(f"\nShared secret established successfully: {secret_A}")
    else:
        print("\nError: Secrets do not match!")

if __name__ == "__main__":
    diffie_hellman()
