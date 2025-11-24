# client.py
import socket
import threading

# -------------------
# RSA helpers
# -------------------
def egcd(a, b):
    if b == 0:
        return (1, 0, a)
    x1, y1, g = egcd(b, a % b)
    return (y1, x1 - (a // b) * y1, g)

def modinv(a, m):
    x, y, g = egcd(a, m)
    if g != 1:
        return None
    return x % m

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def generate_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    # choose e such that 1 < e < phi and gcd(e, phi) == 1
    e = 3
    while e < phi:
        if gcd(e, phi) == 1:
            break
        e += 2
    d = modinv(e, phi)
    if d is None:
        raise ValueError("Failed to find modular inverse for chosen e.")
    return (e, n), (d, n)

def encrypt_message(msg, public_key):
    e, n = public_key
    # encrypt per-character: list of integers
    return [str(pow(ord(ch), e, n)) for ch in msg]

def decrypt_cipher(cipher_list, private_key):
    d, n = private_key
    chars = []
    for c in cipher_list:
        m = pow(int(c), d, n)
        chars.append(chr(m))
    return "".join(chars)

# -------------------
# Network helpers
# -------------------
def recv_line(sock):
    data = b''
    while True:
        part = sock.recv(1)
        if not part:
            return None
        if part == b'\n':
            break
        data += part
    return data.decode()

def listener(sock, private_key):
    peer_pub = None
    while True:
        line = recv_line(sock)
        if line is None:
            print("\n[Connection closed by server]")
            break
        line = line.strip()
        if line.startswith("PEER "):
            _, e_str, n_str = line.split()
            peer_pub = (int(e_str), int(n_str))
            print(f"\n[Info] Received peer public key: {peer_pub}")
            continue
        # Otherwise it's an encrypted message forwarded by server
        # Format: ENC <space-separated integers> or just space-separated ints
        try:
            cipher_parts = line.split()
            # try decrypting
            msg = decrypt_cipher(cipher_parts, private_key)
            print(f"\n[Encrypted Received]: {line}")
            print(f"[Decrypted Message]: {msg}")
        except Exception as ex:
            print(f"\n[Received but failed to decrypt]: {line}   (error: {ex})")

def main():
    server_ip = input("Enter server IP (default 127.0.0.1): ").strip() or "127.0.0.1"
    server_port = int(input("Enter server port (default 5000): ").strip() or 5000)

    # connect
    sock = socket.socket()
    sock.connect((server_ip, server_port))
    print(f"Connected to server {server_ip}:{server_port}")

    # generate keys
    print("\nEnter RSA primes (small primes ok for demo):")
    p = int(input("p: "))
    q = int(input("q: "))
    public_key, private_key = generate_keys(p, q)
    e, n = public_key
    print(f"\nYour Public Key: {public_key}")
    print(f"Your Private Key: {private_key}")

    # send public key to server: format "PUB e n\n"
    sock.sendall(f"PUB {e} {n}\n".encode())

    # start listener thread
    threading.Thread(target=listener, args=(sock, private_key), daemon=True).start()

    # interactive send loop; wait until we receive peer public from server before sending
    peer_public = None
    print("\nType messages to send (type 'exit' to quit). Wait a moment for peer key.")
    while True:
        msg = input("\nMessage: ")
        if msg.lower() == "exit":
            sock.sendall(b"EXIT\n")
            break

        # If we don't have peer public yet, try to read it non-blocking from socket buffer (it will come via listener)
        # For simplicity, ask user to ensure peer key has arrived (listener prints it).
        # You can attempt to send even if peer key isn't known; then server will still relay, but peer can't decrypt.
        # We'll proceed only if user confirms.
        # Here we allow sending anyway; encryption requires peer public key; prompt user:
        confirm = input("Encrypt with peer public key? (y/n/show) ")
        if confirm.lower() == "show":
            print("Your public key:", public_key)
            continue
        if confirm.lower() != "y":
            print("Skipping send.")
            continue

        # We need peer public key — try to read a bit: (listener prints when it arrives)
        # For safety, if no peer key has been received, prompt user to paste peer public key manually (optional)
        # In this simple program, ask the user to input peer public if not received yet:
        # (The listener stores peer key only in its own scope, so prompt manual entry.)
        peer = input("Enter peer public key as 'e n' (or press Enter if you've already got it): ").strip()
        if peer:
            e_peer, n_peer = map(int, peer.split())
            peer_public = (e_peer, n_peer)
        else:
            # If user didn't paste, attempt to proceed: we can't access listener's variable here,
            # so require explicit input or earlier printed PEER message
            try:
                # best-effort: do nothing — user must have seen PEER already
                pass
            except:
                pass

        if peer_public is None:
            print("No peer public key available. You must have received 'PEER e n' from server or enter it manually.")
            continue

        # encrypt per character and send space-separated integers plus newline
        cipher_list = encrypt_message(msg, peer_public)
        cipher_str = " ".join(cipher_list)
        sock.sendall((cipher_str + "\n").encode())
        print("[Encrypted Sent]:", cipher_str)

    sock.close()
    print("Disconnected.")

if __name__ == "__main__":
    main()
