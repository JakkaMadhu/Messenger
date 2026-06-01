import socket
import threading
from config import IP_ADDRESS, PORT_NUMBER
from handlers import handle_client

def main():
    """
    Main server entry point. Binds to configured IP and PORT and listens for TCP client connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((IP_ADDRESS, PORT_NUMBER))
        server_socket.listen()
        print(f"Server started at {IP_ADDRESS}:{PORT_NUMBER}")
        
        while True:
            client_socket, _ = server_socket.accept()
            # Start client socket lifecycle handler in a background daemon thread
            threading.Thread(
                target=handle_client, 
                args=(client_socket,), 
                daemon=True
            ).start()

    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
