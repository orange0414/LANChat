# client.py
import socket
import threading
import sys


def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode("utf-8")
            if not msg:
                break
            print(msg)
        except:
            break


def start_client(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"Connected to server {host}:{port}")

    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.daemon = True
    recv_thread.start()

    try:
        while True:
            msg = input()
            if msg.lower() == "exit":
                break
            client.send(msg.encode("utf-8"))
    except KeyboardInterrupt:
        pass
    finally:
        client.close()
        print("Disconnected.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    start_client(host, port)
