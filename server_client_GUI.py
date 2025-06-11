# server.py
import socket
import threading


''' 
--------------------------------------------------------------------------------------
------WORKER TASK: para el Thread que maneja el socket conectado con cliente----------
--------------------------------------------------------------------------------------
'''
# Funcion que estara corriendo cada Thread que mantiene una conexion
def handle_client(conn, addr, clients):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    # --------------------------------------------------------------------------------
    # --------------------------------FASE INICIAL------------------------------------
    # ---------Pedir el nombre de cliente y avisar a todo el mundo del chat-----------
    #---------------------------------------------------------------------------------
    conn.send(f"<span style = 'color:green'>[Server]: First message should be your nickname.</span><br>".encode("utf-8"))
    nickname = conn.recv(1024).decode("utf-8") 
    
    clients[conn] = nickname
    
    server_msg  = (f"<span style = 'color:green;'>[Server]:</span> "
                   f"<span style = 'color:cyan;'>{nickname}</span> "
                   f"<span style = 'color:green;'>ha entrado al chat.</span><br>")
    server_broadcast(server_msg, clients)
    server_msg = (f"<span style = 'color:green;'>[Server]: Continuaras como</span> "
                  f"<span style = 'color:cyan;'>{nickname} </span><br>")
    conn.send(server_msg.encode('utf-8'))
    # --------------------------------------------------------------------------------
    # --------------------------------ESTABLISHED-------------------------------------
    # --------------------------------------------------------------------------------
    while True:
        try:
            msg = conn.recv(1024).decode("utf-8")   # lee los bits que envia, y con un maximo de 1024 bytes, bloqueante
            if not msg: # Si en el otro extremo llama a close() entonces devuelveria b''(bytes vacio)
                break
            client_broadcast(msg, conn, clients)
        except ConnectionResetError:
            break
    
    # --------------------------------------------------------------------------------
    # ----------------------------------DESCONEXION----------------------------------
    # --------------------------------------------------------------------------------
    print(f"[DISCONNECT] {addr} disconnected.")
    server_msg = f"<span style = 'color:green;'>[Server]:</span> "f"<span style = 'color:cyan;'>{nickname}</span> ha salido del chat.<br>"
    server_broadcast(server_msg, clients)
    del clients[conn]
    conn.close()

def server_broadcast(server_msg, clients):
    for client in clients.keys():
        try:
            client.send(server_msg.encode("utf-8"))
        except:
            pass
        
def client_broadcast(message, sender_conn, clients):
    for client in clients.keys():
        if not client == sender_conn:
            html_msg = f"<span style='color: cyan;'>[{clients[sender_conn]}]:</span> "f"{message}<br>"
            try:
                client.send(html_msg.encode("utf-8"))
            except:
                pass
        elif client == sender_conn:
            html_msg = f"<span style='color: cyan; font-weight:bold;'>[{clients[sender_conn]}]</span>: "f"{message}<br>"
            try:
                client.send(html_msg.encode("utf-8"))
            except:
                pass

'''
-------------------------------------------------------------------------------------
-----SERVER TASK: Escuchar y crear sockets para mantener contacto con cliente--------
-------------------------------------------------------------------------------------
'''
def start_server(host="0.0.0.0", port=5555):
    backlog = 5     # numero de peticiones que pueden estar esperando a la vez
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # AF_INET: IPv4, STREAM: TCP
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Para reutilizar el direccion/port sin necesidad de que lo libere
    server.bind((host, port))   # Asociar un host y port al server
    '''
    Empieza a escuchar conexiones, solo configura el socket como server, pero no es bloqueante. 
    Si hay "backlog=%%" peticiones a la vez, y llega uno nuevo, se rechazara. 
    El numero de backlog default es de 128
    '''
    server.listen(backlog)
    print(f"[LISTENING] Server is listening on {host}:{port}")
    if host == '0.0.0.0':
        lan_ip = get_local_ip()
        print(f"[INFO] Other LAN devices should connect to {lan_ip}:{port}")
        
    clients = {}    # dict[socket.socket, nickname]
    while True:
        conn, addr = server.accept()  # Es bloqueante, espera la conexion
        
        
        
        thread = threading.Thread(target=handle_client, args=(conn, addr, clients))
        thread.daemon = True
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(clients)}")

def get_local_ip():
    """Mediante UDP encontramos la IP del host dentro de LAN"""
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # DGRAM: UDP
    try:
        temp_sock.connect(('255.255.255.255', 1))
        ip = temp_sock.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        temp_sock.close()
    return ip

if __name__ == "__main__":
    start_server()
