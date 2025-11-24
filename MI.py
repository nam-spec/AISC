# mod_inverse_with_table.py

def extended_euclid_table(a, b):
    print(f"{'q':>5} {'r1':>8} {'r2':>8} {'r':>8} {'s1':>8} {'s2':>8} {'s':>8} {'t1':>8} {'t2':>8} {'t':>8}")
    print("-" * 95)

    r1, r2 = a, b
    s1, s2 = 1, 0
    t1, t2 = 0, 1

    while r2 != 0:
        q = r1 // r2
        r = r1 % r2
        s = s1 - q * s2
        t = t1 - q * t2

        print(f"{q:>5} {r1:>8} {r2:>8} {r:>8} {s1:>8} {s2:>8} {s:>8} {t1:>8} {t2:>8} {t:>8}")

        # shift rows down
        r1, r2 = r2, r
        s1, s2 = s2, s
        t1, t2 = t2, t

    print("\nGCD =", r1)
    print("s =", s1, ", t =", t1)
    return r1, s1, t1


def mod_inverse(a, m):
    print("\n--- Extended Euclid Table ---")
    g, x, y = extended_euclid_table(a, m)

    if g != 1:
        print("\nMultiplicative inverse does NOT exist.")
        return None

    inv = x % m
    print(f"\nMultiplicative inverse of {a} mod {m} = {inv}")
    return inv


def main():
    a = int(input("Enter a: "))
    m = int(input("Enter modulus m: "))

    mod_inverse(a, m)


if __name__ == "__main__":
    main()