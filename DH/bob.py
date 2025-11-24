import socket
import random

def bob():
# Bob chooses prime p and primitive root g
    p = int(input("Enter prime number p: "))
    g = int(input("Enter primitive root g: "))
    
    # Bob chooses a private key
    b = random.randint(2, p - 2)
    print(f"Bob private key: {b}")

    # Bob's public value
    B = pow(g, b, p)
    print(f"Bob public value sent to Alice: {B}")

    # Socket setup
    s = socket.socket()
    s.bind(("127.0.0.1", 5000))
    s.listen(1)

    print("Waiting for Alice to connect...")
    conn, addr = s.accept()
    print(f"Alice connected from: {addr}")

    # Send p, g, B to Alice
    conn.send(f"{p},{g},{B}".encode())

    # Receive Alice's public key
    A = int(conn.recv(1024).decode())
    print(f"Received Alice public value: {A}")

    # Compute shared secret
    shared_secret = pow(A, b, p)
    print(f"Shared secret (Bob): {shared_secret}")

    conn.close()
    s.close()

if __name__ == "__main__":
    bob()