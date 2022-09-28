import socket
import pickle

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = "192.168.1.9"
        self.port = 5555
        self.address = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        print(type(self.p))
        return self.p

    def connect(self):
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data: str):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)