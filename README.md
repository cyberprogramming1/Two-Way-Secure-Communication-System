# Two-Way Secure Communication System

## Overview
This project implements a two-way secure communication system using Python's socket and SSL libraries. The system consists of a proxy server and multiple clients, allowing users to send text messages and image files securely over the network.

## Features
- **Secure Communication**: Utilizes SSL to ensure encrypted data transfer between clients and the server.
- **Text Messaging**: Users can send and receive text messages in real-time.
- **File Transfer**: Users can send image files to each other.
- **Multi-client Support**: Multiple clients can connect to the server and communicate simultaneously.

## Requirements
- Python
- Required Python libraries:
  - `socket`
  - `ssl`
  - `threading`
  - `os`
- [Chocolatey](https://chocolatey.org/) (for Windows users)

## Installation
1. **Install Chocolatey** (if not already installed) using PowerShell as an administrator:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
   ```

2. **Install OpenSSL** using Chocolatey:
   ```powershell
   choco install openssl --confirm
   ```

3. Clone the repository:
   ```bash
   git clone https://github.com/cyberprogramming1/Two-Way-Secure-Communication-System.git
   cd Secure-Communication-System
   ```

4. **Generate SSL certificates**:
   ```bash
   cd C:\Users\path\Secure-Communication-System
   
   openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key
   ```

5. Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

## Usage

### Starting the Proxy Server
Run the proxy server script on your desired host machine:
```bash
python server.py
```
This will start the server and listen for incoming client connections.

### Starting the Client
Run the client script on different machines or terminal windows:
```bash
python client.py
```
- Enter a username when prompted.
- Use `/send <filepath>` to send an image file.
- Type any text message to send it to other connected users.
- Type `bye` to exit the chat.

## Code Structure
- **server.py**: The main server code that handles incoming client connections and message broadcasting.
- **client.py**: The client code that allows users to connect to the server, send messages, and transfer files.

## File Transfer Protocol
- When sending an image, the client sends a command starting with `file:` followed by the filename.
- The server receives the file in chunks and saves it as `received_<filename>`.

## Example
1. Start the proxy server.
2. Connect multiple clients, each entering a unique username.
3. Clients can send messages or image files to each other seamlessly.

## Error Handling
The application includes basic error handling to manage connection issues and file transfer errors. Any exceptions will be printed to the console for debugging purposes.

## Acknowledgments
- This project uses the SSL library for secure communication.
- Inspired by various open-source communication protocols.
