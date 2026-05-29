import socket
import json
import threading
from config import DEFAULT_HOST, DEFAULT_PORT

class Client:
    """
    Handles socket network connection, data sending, and background message listening.
    """
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.socket = None
        self.listener_thread = None
        self.running = False
        self.callback = None

    def connect(self, callback):
        """
        Connects to the socket server and starts the background listening thread.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.running = True
            self.callback = callback
            self.listener_thread = threading.Thread(target=self._listen_loop, args=(self.socket,), daemon=True)
            self.listener_thread.start()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def send(self, data):
        """
        Sends JSON serialized data to the server.
        """
        if not self.socket or not self.running:
            return False
        try:
            raw_data = json.dumps(data) + '\n'
            self.socket.sendall(raw_data.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Send error: {e}")
            self.disconnect()
            return False

    def _listen_loop(self, socket_connection):
        """
        Daemon thread loop. Continuously reads JSON payload lines from the server.
        """
        try:
            reader = socket_connection.makefile('r', encoding='utf-8')
            while self.running and self.socket == socket_connection:
                line = reader.readline()
                if not line:
                    break
                try:
                    data = json.loads(line.strip())
                    if self.callback:
                        self.callback(data)
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            print(f"Listener thread error: {e}")
        finally:
            self._cleanup_socket(socket_connection)

    def _cleanup_socket(self, socket_connection):
        try:
            socket_connection.close()
        except:
            pass
        if self.socket == socket_connection:
            self.running = False
            self.socket = None

    def disconnect(self):
        """
        Disconnects the socket and terminates background listeners.
        """
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
