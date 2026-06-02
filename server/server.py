import socket
import threading
import logging
from config import IP_ADDRESS, PORT_NUMBER
from handlers import handle_client

# Configure root logger to output formatted logs to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    """
    Main server entry point. Binds to configured IP and PORT and listens for TCP client connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((IP_ADDRESS, PORT_NUMBER))
        server_socket.listen()
        logger.info(f"Server started at {IP_ADDRESS}:{PORT_NUMBER}")
        
        while True:
            client_socket, _ = server_socket.accept()
            # Start client socket lifecycle handler in a background daemon thread
            threading.Thread(
                target=handle_client, 
                args=(client_socket,), 
                daemon=True
            ).start()

    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    except Exception as e:
        logger.exception(f"Server encountered a fatal error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
