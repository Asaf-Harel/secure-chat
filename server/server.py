import socket
from _thread import *
import sys
from utils.RSA import *
import pickle
from utils import users


class Server:
    def __init__(self, ip_addr, port):
        self.ip_addr = ip_addr
        self.port = port

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server.bind((self.ip_addr, self.port))

        self.__list_of_clients = []

        rsa = RSA()
        self.public_key, self.__private_key = rsa.generate_keys()

    def start(self):
        self.__server.listen(100)
        print(f'chatroom started at: {self.ip_addr}:{self.port}')

        while True:
            try:
                conn, addr = self.__server.accept()

                self.__list_of_clients.append((conn, addr))

                # prints the address of the user that just connected
                print(addr[0] + " connected")

                # creates and individual thread for every user that connects
                start_new_thread(self.__client_thread, (conn, addr))

            except KeyboardInterrupt:
                print('Shutting down...')
                break

        conn.close()
        self.__server.close()

    def __client_thread(self, conn, addr):
        self.__greet(conn, addr)
        conn.send('Welcome to the chatroom!\n'.encode('utf-8'))

        while True:
            try:
                message = conn.recv(2048)
                message = pickle.loads(message)
                message = decrypt(message, self.__private_key)

                if message:
                    print(f"<{addr[0]}> {message}")

                    # Calls broadcast function to send message to all
                    message_to_send = f"<{addr[0]}> {message}"
                    self.__broadcast(message_to_send, conn)

                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    self.__remove((conn, addr))
            except:
                continue

    def __greet(self, conn, addr):
        # sends a message to the client whose user object is conn
        while True:
            conn.send(f'{self.public_key[0]} {self.public_key[1]}'.encode('utf-8'))  # Send server public key

            msg = conn.recv(2048)  # Get confirmation
            msg = msg.decode()

            if msg.isnumeric():
                code = int(msg)
                if code == 200:
                    conn.send('200'.encode('utf-8'))
                    break

        key_msg = conn.recv(2048)  # Get client public key
        key_msg = key_msg.decode()
        key = tuple([int(num) for num in key_msg.split(' ')])

        users.insert(addr[0], key)
        # conn.send('200'.encode('utf-8'))  # Send Confirmation

    def __broadcast(self, msg, conn):
        for clients in self.__list_of_clients:
            try:
                key = users.get_key(clients[1][0])
                encrypted = encrypt(msg, key)
                clients[0].send(pickle.dumps(encrypted))
            except:
                clients[0].close()
                self.__remove(clients)

    def __remove(self, client):
        if client in self.__list_of_clients:
            self.__list_of_clients.remove(client[0])
            print(client[1][0], 'disconnected')


ip_address = socket.gethostbyname_ex(socket.gethostname())[2][0]
port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

server = Server(ip_address, port)
server.start()
