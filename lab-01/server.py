# import socket module
from socket import *
import threading
import sys  # In order to terminate the program

def send_data(connectionSocket, outputdata):
    for i in range(0, len(outputdata)):
        connectionSocket.send(outputdata[i].encode())
    connectionSocket.send("\r\n".encode())

def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata =  f.read() # read file
        # Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        # Send the content of the requested file to the client
        send_data(connectionSocket, outputdata)
    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        f = open('404.html')
        outputdata = f.read()
        send_data(connectionSocket, outputdata)
    # Close client socket
    connectionSocket.close()

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a sever socket
    serverPort = 12000
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr =  serverSocket.accept()
        try:
            # Create a thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
            client_thread.start()
        except KeyboardInterrupt:
            serverSocket.close()
            sys.exit()  # Terminate the program

    serverSocket.close()
    sys.exit()  # Terminate the program

if __name__ == "__main__":
    main()