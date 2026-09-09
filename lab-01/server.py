from socket import *
import threading
import sys

def handle_client(connectionSocket):
    thread_id = threading.get_ident()   # Get the thread ID for debug
    print(f"[DEBUG] Client connected on thread ID: {thread_id}")
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])  # Open file
        outputdata =  f.read()  # Read file
        # Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        # Send the content of the requested file to the client
        connectionSocket.sendall(outputdata.encode())
    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        # Send the content of the 404 error page to the client
        f = open('404.html')
        outputdata = f.read()
        connectionSocket.sendall(outputdata.encode())
    print(f"[DEBUG] Client closed on thread ID: {thread_id}")
    # Close client socket
    connectionSocket.close()

def main():
    # Prepare a sever socket
    serverSocket = socket(AF_INET, SOCK_STREAM) # Create a TCP socket
    serverAddress = ''
    serverPort = 12000
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Allow reuse of the address
    serverSocket.bind((serverAddress, serverPort)) # Bind the socket to the server address and server port
    serverSocket.listen() # Listen for incoming connections

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

if __name__ == "__main__":
    main()