import socket
import random

def alice():
    s = socket.socket()
    s.connect(("127.0.0.1", 5000))

    # Receive p, g, B from Bob
    data = s.recv(1024).decode()
    p, g, B = map(int, data.split(","))
    print(f"Received from Bob -> p={p}, g={g}, B={B}")

    # Alice chooses a private key
    a = random.randint(2, p - 2)
    print(f"Alice private key: {a}")

    # Alice public value
    A = pow(g, a, p)
    print(f"Alice public value sent to Bob: {A}")

    # Send A back to Bob
    s.send(str(A).encode())

    # Compute shared secret
    shared_secret = pow(B, a, p)
    print(f"Shared secret (Alice): {shared_secret}")

    s.close()

if __name__ == "__main__":
    alice()