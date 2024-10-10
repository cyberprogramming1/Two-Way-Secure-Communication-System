import socket
import ssl
import threading
import os

clients = {}

def handle_client(client_socket, username):
    """Function to handle communication with a connected client."""
    try:
        while True:
            
            message = client_socket.recv(1024).decode()
            if not message:
                break 
            if message.startswith("file:"):
                filename = message.split("file:")[1].strip()
                filesize = int(client_socket.recv(1024).decode())

                with open(f"received_{filename}", 'wb') as f:
                    bytes_received = 0
                    while bytes_received < filesize:
                        chunk = client_socket.recv(4096)
                        if not chunk:
                            break
                        f.write(chunk)
                        bytes_received += len(chunk)

                print(f"Received file: {filename} from {username}")
                
                recipient = username  
                broadcast_file(filename, recipient)
            else:
                print(f"{username}: {message}")
                if message.lower() == "bye":
                    break  # Exit the loop if the user says bye
                broadcast(f"{username}: {message}", client_socket)
    except Exception as e:
        print(f"Client handling error: {e}")
    finally:
        print(f"{username} disconnected.")
        del clients[client_socket]  
        broadcast(f"{username} has left the chat.", client_socket) 
        client_socket.close()

def broadcast_file(filename, recipient):
    """Send a file to a specific client."""
    for client_socket, user in clients.items():
        if user == recipient:
            client_socket.send(f"file:{filename}".encode())
            client_socket.send(str(os.path.getsize(filename)).encode())
            with open(f"received_{filename}", 'rb') as f:
                while (chunk := f.read(4096)):
                    client_socket.sendall(chunk)
            print(f"Sent file: {filename} to {recipient}")

def broadcast(message, sender_socket):
    """Send a message to all clients except the sender."""
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message.encode())

def start_proxy_server():
    """Function to start the proxy server."""
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(('0.0.0.0', 65432))  # Listen on all interfaces
    proxy_socket.listen(5)  # Max 5 clients waiting to connect
    print("Proxy server started, waiting for connections...")

    while True:
        try:
            client_socket, addr = proxy_socket.accept()
            secure_socket = context.wrap_socket(client_socket, server_side=True)

            # Receive username
            username = secure_socket.recv(1024).decode()
            clients[secure_socket] = username
            print(f"Client {username} connected from {addr}")

            # Start a new thread for each client
            threading.Thread(target=handle_client, args=(secure_socket, username)).start()

        except Exception as e:
            print(f"Error accepting connections: {e}")

if __name__ == "__main__":
    start_proxy_server()