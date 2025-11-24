def extended_gcd(a, b):
    r1, r2 = a, b
    s1, s2 = 1, 0
    t1, t2 = 0, 1

    print("q\tr1\tr2\tr\ts1\ts2\tt1\tt2")

    while r2 != 0:
        q = r1 // r2
        r = r1 % r2
        
        print(f"{q}\t{r1}\t{r2}\t{r}\t{s1}\t{s2}\t{t1}\t{t2}")
        
        r1, r2 = r2, r
        s1, s2 = s2, s1 - q * s2
        t1, t2 = t2, t1 - q * t2

# Final result
    print(f"GCD is {r1}")
    print(f"Coefficients: x = {s1}, y = {t1}")
    return r1, s1, t1

print(extended_gcd(28,5))