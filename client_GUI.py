import sys
import socket
from PyQt6 import QtWidgets, QtCore

'''
--------------------------------------------
-------------RECEIVER TASK------------------
--------------------------------------------
'''
class ReceiverThread(QtCore.QThread):
    message_received = QtCore.pyqtSignal(str)

    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.running = True

    def run(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                text = data.decode('utf-8')
                self.message_received.emit(text)
            except OSError:
                break

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

'''
--------------------------------------------------
---------------Main Window------------------------
--------------------------------------------------
'''
class ChatClientGUI(QtWidgets.QMainWindow):
    def __init__(self, host, port):
        super().__init__()
        self.setWindowTitle(f"Chat Client - {host}:{port}")

        # Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # Widgets
        self.chat_display = QtWidgets.QTextEdit()
        self.chat_display.setReadOnly(True)
        self.input_line = QtWidgets.QLineEdit()
        self.send_button = QtWidgets.QPushButton("Enviar")

        # Layout
        central = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout(central)   # asociarlo al central Widget
        vbox.addWidget(self.chat_display)
        hbox = QtWidgets.QHBoxLayout()  # hbox para donde edita el exto para enviar
        hbox.addWidget(self.input_line)
        hbox.addWidget(self.send_button)
        vbox.addLayout(hbox)
        self.setCentralWidget(central)

        # Conexiones
        self.send_button.clicked.connect(self.send_message)
        self.input_line.returnPressed.connect(self.send_message)

        # Hilo receptor
        self.receiver = ReceiverThread(self.sock)
        self.receiver.message_received.connect(self.on_message)
        self.receiver.start()

    '''SENDER FUNCTION'''
    def send_message(self):
        msg = self.input_line.text().strip()
        if not msg:
            return
        try:
            self.sock.send(msg.encode('utf-8'))
        except OSError:
            pass
        self.input_line.clear()

    '''SHOW RECEIVED MESSAGE'''
    def on_message(self, text):
        # Añadir mensaje al display sin interferir con la entrada
        self.chat_display.append(text)
        
    '''
    Sobreescribe la funcion de closeEvent para poder cerrar el socket antes de cerra
    el MainWindow
    '''
    def closeEvent(self, event):
        # Detener el hilo receptor primero
        try:
            # Interrumpir el recv bloqueante (tambien al envio: RD_read, WR_write)
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.receiver.stop()
        # Cerrar el socket
        try:
            self.sock.close()
        except OSError:
            pass
        # Llamar al manejador base para un cierre apropiado
        super().closeEvent(event)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Escribe algo como: python chat_client_gui.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])

    app = QtWidgets.QApplication(sys.argv)
    window = ChatClientGUI(host, port)
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
