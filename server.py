# server.py
import socket
import threading


# --------------------------------------------------------------------------------------
# ------Para Thread y Socket conectados con cliente-------------------------------------
# --------------------------------------------------------------------------------------
# Funcion que estara corriendo cada Thread que mantiene una conexion
def handle_client(conn, addr, clients):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("First message should be your nickname.".encode("utf-8"))
    nickname = conn.recv(256).decode("utf-8")
    conn.send((f"Received Nickname: {nickname} \nYou can send broadcasts now.").encode("utf-8"))
    while True:
        try:
            msg = conn.recv(1024).decode("utf-8")   # lee los bits que envia, y con un maximo de 1024 bits, bloqueante
            if not msg:
                break
            broadcast(nickname, msg, conn, clients)
        except ConnectionResetError:
            break
    print(f"[DISCONNECT] {addr} disconnected.")
    clients.remove(conn)
    conn.close()


def broadcast(nickename, message, sender_conn, clients):
    for client in clients:
        if client != sender_conn:
            try:
                screen_msg = (f"[{nickename}]: {message}")
                client.send(screen_msg.encode("utf-8"))
            except:
                pass


# -------------------------------------------------------------------------------------
# -----------Para el Server que esta escuchando----------------------------------------
# -------------------------------------------------------------------------------------
def start_server(host="0.0.0.0", port=5555):
    backlog = 5  # numero de peticiones que pueden estar esperando a la vez
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Para reutilizar el direccion/port despues de que se cierre el server, sin necesidad de que lo libere
    server.bind((host, port))  # Asociar un host y port al server
    server.listen(backlog)  # Empieza a escuchar conexiones, solo configura el socket como server, pero no es bloqueante. Si hay "backlog=%%"
    # peticiones a la vez, y llega uno nuevo, se rechazara. El numero de backlog default es de 128
    print(f"[LISTENING] Server is listening on {host}:{port}")

    clients = []
    while True:
        conn, addr = server.accept()  # Es bloqueante, espera la conexion
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr, clients))
        thread.daemon = True
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(clients)}")


if __name__ == "__main__":
    start_server()
