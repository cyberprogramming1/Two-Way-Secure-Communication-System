import socket
import ssl
import threading
import os

exit_event = threading.Event()  

def listen_for_messages(secure_socket):
    """Function to listen for incoming messages and files from the proxy server."""
    while not exit_event.is_set():  
        try:
            response = secure_socket.recv(1024).decode()
            if response.startswith("file:"):
                
                filename = response.split("file:")[1].strip()
                filesize = int(secure_socket.recv(1024).decode())

                
                with open(f"received_{filename}", 'wb') as f:
                    bytes_received = 0
                    while bytes_received < filesize:
                        chunk = secure_socket.recv(4096)
                        if not chunk:
                            break
                        f.write(chunk)
                        bytes_received += len(chunk)

                print(f"\nReceived file: {filename}")
            else:
                print(f"\n{response}")
        except Exception as e:
            if exit_event.is_set(): 
                break
            print(f"Error receiving message: {e}")
            break

def send_image(secure_socket, filepath):
    """Function to send an image file to the server."""
    if os.path.exists(filepath):
        filename = os.path.basename(filepath)
        secure_socket.send(f"file:{filename}".encode())  
        secure_socket.send(str(os.path.getsize(filepath)).encode()) 

        
        with open(filepath, 'rb') as f:
            while (chunk := f.read(4096)):
                secure_socket.sendall(chunk)

        print(f"Sent file: {filename}")
    else:
        print(f"File '{filepath}' not found.")

def parse_file_command(command):
    """Function to parse the file path command with support for quoted file paths."""
    if command.startswith('/send '):
        if '"' in command:
            filepath = command.split('"')[1].strip()
        else:
            filepath = command.split('/send ')[1].strip()
        return filepath
    return None

def start_client():
    """Function to start the client and establish communication."""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    username = input("Enter your username: ")

    try:
        client_socket = socket.create_connection(('IP_ADDR', 65432))#please change IP_ADDR with you Server IP
        secure_socket = context.wrap_socket(client_socket, server_hostname='IP_ADDR')
        print("Connected to the proxy server.")

        secure_socket.send(username.encode())

        # Start a thread to listen for incoming messages and files
        threading.Thread(target=listen_for_messages, args=(secure_socket,), daemon=True).start()

        while True:
            message = input('You (text or "/send <filepath>"): ')

            if message.startswith('/send '):
                filepath = parse_file_command(message)
                if filepath:
                    send_image(secure_socket, filepath)
                else:
                    print("Invalid file path. Use quotes for paths with spaces.")
            else:
                secure_socket.send(message.encode())

            if message.lower() == 'bye':
                print("Exiting chat...")
                break

    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        exit_event.set()  # Set the exit flag to signal the thread to exit
        secure_socket.close()
        print("Disconnected from the server.")

if __name__ == "__main__":
    start_client()
