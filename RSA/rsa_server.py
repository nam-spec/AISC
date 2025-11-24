# server.py
import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = {}   # client_id -> (conn, addr, public_key_tuple)

lock = threading.Lock()

def recv_line(conn):
    """Receive a newline-terminated message (or until socket ends)."""
    data = b''
    while True:
        part = conn.recv(1)
        if not part:
            return None
        if part == b'\n':
            break
        data += part
    return data.decode()

def handle_client(client_id, conn, addr):
    global clients
    try:
        # Step 1: Receive client's public key in format: PUB e n\n
        line = recv_line(conn)
        if line is None:
            return
        line = line.strip()
        if not line.startswith("PUB "):
            conn.sendall(b"ERR expected PUB\n")
            conn.close()
            return
        _, e_str, n_str = line.split()
        e = int(e_str); n = int(n_str)
        with lock:
            clients[client_id] = (conn, addr, (e, n))
        print(f"[Server] Received public key from client {client_id}: (e={e}, n={n})")

        # Wait until both clients are connected and have provided keys
        while True:
            with lock:
                if len(clients) >= 2 and all(clients.get(i) is not None for i in (1,2)):
                    break

        # Send peer public key
        with lock:
            for other_id, (oconn, oaddr, opub) in clients.items():
                if other_id != client_id:
                    oe, on = opub
                    conn.sendall(f"PEER {oe} {on}\n".encode())
                    print(f"[Server] Sent peer public key to client {client_id}: (e={oe}, n={on})")
                    break

        # Now relay loop: receive encrypted lines and forward to other client
        while True:
            line = recv_line(conn)
            if line is None:
                break
            line = line.strip()
            if line == "":
                continue
            # Expecting ENC ... or EXIT
            if line == "EXIT":
                break
            # Otherwise forward raw encrypted message to other client
            with lock:
                for other_id, (oconn, oaddr, opub) in clients.items():
                    if other_id != client_id:
                        try:
                            oconn.sendall((line + "\n").encode())
                        except:
                            pass
            print(f"[Server] Relayed from client {client_id}: {line}")

    except Exception as ex:
        print(f"[Server] Error with client {client_id}: {ex}")
    finally:
        with lock:
            if client_id in clients:
                del clients[client_id]
        try:
            conn.close()
        except:
            pass
        print(f"[Server] Client {client_id} disconnected")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"[Server] Listening on {HOST}:{PORT}. Waiting for 2 clients...")

    client_id = 1
    while client_id <= 2:
        conn, addr = server.accept()
        print(f"[Server] Client {client_id} connected from {addr}")
        threading.Thread(target=handle_client, args=(client_id, conn, addr), daemon=True).start()
        client_id += 1

    # keep server alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[Server] Shutting down")
        server.close()

if __name__ == "__main__":
    main()
