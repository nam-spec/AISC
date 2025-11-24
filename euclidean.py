def gcd(a, b):
    if a < b:
        a, b = b, a

    q, r = 0, 0

    print("q\tr1\tr2\tr")
    while b != 0:
        q = a // b
        r = a % b
        print(f"{q}\t{a}\t{b}\t{r}")
        a, b = b, r

    return a

print(gcd(100, 110))