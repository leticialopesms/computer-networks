# import socket module
from socket import *
import threading
import sys  # In order to terminate the program

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

def handle_thread(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata =  f.read() # read file
        # Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
    connectionSocket.close()

def main():
    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr =  serverSocket.accept()
        client_thread = threading.Thread(
            target=handle_thread,
            args=(connectionSocket,)
        )
        client_thread.start()
        client_thread.join()
        # sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    main()