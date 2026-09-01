# import socket module
from socket import *
import threading
import sys  # In order to terminate the program

def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata =  f.read() # Read file
        # Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        # Send the content of the requested file to the client
        connectionSocket.sendall(outputdata.encode())
    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        f = open('404.html')
        outputdata = f.read()
        connectionSocket.sendall(outputdata.encode())
    # Close client socket
    connectionSocket.close()

def main():
    # Prepare a sever socket
    serverSocket = socket(AF_INET, SOCK_STREAM) # Create a TCP socket
    serverAddress = ''
    serverPort = 12000
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Allow reuse of the address
    serverSocket.bind((serverAddress, serverPort)) # Bind the socket to the server address and server port
    serverSocket.listen(1) # Listen for incoming connections

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr =  serverSocket.accept()
        try:
            # Create a thread to handle the client connection
            client_thread = threading.Thread(
                target=handle_client,
                args=(connectionSocket,)
            )
            client_thread.start()
        except KeyboardInterrupt:
            serverSocket.close()
            sys.exit()  # Terminate the program

    serverSocket.close()
    sys.exit()  # Terminate the program

if __name__ == "__main__":
    main()