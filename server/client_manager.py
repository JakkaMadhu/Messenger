import json
import threading
import logging

logger = logging.getLogger(__name__)

def send_json(client_socket, data):
    """
    Sends a JSON payload over a socket, followed by a newline separator.
    """
    try:
        raw_data = json.dumps(data) + '\n'
        client_socket.sendall(raw_data.encode('utf-8'))
    except Exception as e:
        logger.error(f"Error sending JSON data: {e}")

class ClientManager:
    """
    Manages active socket client connections with thread-safe operations.
    """
    def __init__(self):
        self._clients = {}  # key: email, value: {"socket": client_socket, "name": name}
        self._lock = threading.RLock()

    def add_client(self, email, client_socket, name):
        with self._lock:
            self._clients[email.lower()] = {"socket": client_socket, "name": name}
        logger.info(f"User logged in: {email}")
        self.broadcast_online_users()

    def remove_client(self, email, client_socket):
        with self._lock:
            email_lower = email.lower()
            if email_lower in self._clients and self._clients[email_lower]["socket"] == client_socket:
                self._clients.pop(email_lower, None)
                logger.info(f"User logged out/disconnected: {email}")
                self.broadcast_online_users()
            else:
                logger.info(f"Disconnect cleanup ignored for {email} (socket was replaced).")

    def get_receiver_socket(self, email):
        with self._lock:
            client_info = self._clients.get(email.lower())
            return client_info["socket"] if client_info else None

    def get_online_users(self):
        with self._lock:
            return [{"email": email, "name": info["name"]} for email, info in self._clients.items()]

    def get_sockets_except(self, exclude_email):
        with self._lock:
            exclude_lower = exclude_email.lower()
            return [info["socket"] for email, info in self._clients.items() if email != exclude_lower]

    def broadcast_online_users(self):
        with self._lock:
            online_list = self.get_online_users()
            data = {"status": "online_users", "users": online_list}
            sockets_to_send = [info["socket"] for info in self._clients.values()]
        for client_socket in sockets_to_send:
            send_json(client_socket, data)
