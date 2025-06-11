# Chat en LAN Local

Este proyecto implementa un sistema de chat básico en una pequeña red de área local (LAN) utilizando sockets de Python. Incluye tanto una interfaz de línea de comandos (CLI) como una interfaz gráfica basada en Qt (PyQt6), permitiendo a los usuarios comunicarse en tiempo real.

## Estructura de Archivos

- **server.py**\
  Servidor principal en CLI que acepta múltiples conexiones de clientes, gestiona apodos y reenvía mensajes a todos los clientes conectados.

- **client.py**\
  Cliente en CLI que se conecta al servidor, envía y recibe mensajes de otros participantes. Permite desconexión segura al escribir `exit`.

- **client\_GUI.py**\
  Cliente con interfaz gráfica (PyQt6). Proporciona una ventana con un área de texto para mostrar el chat y un campo de entrada para enviar mensajes. Lanza un hilo dedicado para recibir mensajes sin bloquear la UI.\
  Dependencia: `PyQt6`.

- **server\_client\_GUI.py**\
  Versión del servidor idéntica a `server.py`. Está preparada para integrarse con clientes GUI o futuras extensiones de administración gráfica.

## Características

- Conexión TCP/IP punto a punto en LAN.
- Soporte para múltiples clientes concurrentes usando hilos (threading).
- Gestión de apodos: cada cliente indica su nickname al conectarse.
- Difusión de mensajes: el servidor reenvía los mensajes recibidos a todos los demás clientes.
- Interfaz gráfica (PyQt6) opcional para el cliente.
- Cierre limpio de conexiones y hilos al desconectar.

## Requisitos

- Python 3.7 o superior.
- Paquete `PyQt6` (solo para la parte GUI):
  ```sh
  pip install PyQt6
  ```

## Uso

1. Inicia el servidor en tu máquina LAN (por defecto en el puerto 5555):

   ```sh
   python server.py
   ```

   O bien, para la versión genérica:

   ```sh
   python server_client_GUI.py
   ```

2. Conecta clientes por CLI:

   ```sh
   python client.py <host> <port>
   ```

   Ejemplo:

   ```sh
   python client.py 192.168.1.100 5555
   ```

3. Conecta clientes con GUI:

   ```sh
   python client_GUI.py <host> <port>
   ```

   Ejemplo:

   ```sh
   python client_GUI.py localhost 5555
   ```

4. Cada cliente debe escribir su nickname como primer mensaje. Luego, puede enviar textos que serán enviados al resto de participantes.

5. Para salir en CLI, escribe `exit` y confirma con `y`. En GUI, cierra la ventana.

## Arquitectura

- **Servidor** crea un socket TCP y acepta conexiones en un bucle infinito. Cada conexión se maneja en un nuevo hilo, que gestiona recepción de mensajes y notificaciones de entrada/salida.
- **Cliente CLI** lanza un hilo para recibir mensajes de forma asíncrona y mantiene el bucle de lectura de entradas del usuario.
- **Cliente GUI** utiliza `QThread` para recibir mensajes en segundo plano y señales Qt para actualizar la interfaz.
