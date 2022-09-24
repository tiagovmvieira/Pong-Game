import socket
from _thread import *
import sys

class Server():
    def __init__(self):
        self.server = ""
        self.port = 5555

    @staticmethod
    def setup_socket():
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind_server_on_port(self, skt: socket):
        try:
            skt.bind((self.server, self.port))
        except socket.error as e:
            str(e)

    def listen_for_connections(self, skt: socket, no_clients: int = None):
        if no_clients:
            skt.listen(no_clients)
        else:
            skt.listen()        
        print("Waiting for a connection, Server Started!")

    def threaded_client(self, connection):
        print(type(connection))
        reply = ""
        while True:
            try:
                data = connection.recv(2048)
                reply = data.decode('utf-8')

                if not data:
                    print("Client disconnected from the Server")
                    break
                else:
                    print("Recieved: ", reply)
                    print("Sending: ", reply)

                connection.sendall(str.encode(reply)) # encode into a bytes object
            except:
                break

if __name__ == '__main__':
    server = Server()
    skt = server.setup_socket()
    server.bind_server_on_port(skt)
    server.listen_for_connections(skt, 2)

    while True:
        connection, address = skt.accept() #accept any incoming connections into our server (connection and adress (ip))
        print("Connected to:", address)

        start_new_thread(server.threaded_client(connection))



