import socket
import select
import sys
from utils.RSA import *
from utils import keys
import pickle


def ___are_equal(string: str, num: int):
    if string.isnumeric():
        code = int(string)
        return code == num
    return False


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) < 2:
    print("Correct usage: script, IP address")
    exit()

IP_address = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

server.connect((IP_address, port))

key = None

if not keys.read():
    rsa = RSA()
    public_key, private_key = rsa.generate_keys()
else:
    public_key, private_key = keys.get_keys()

while True:
    try:
        # maintains a list of possible input streams
        sockets_list = [sys.stdin, server]

        read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)

                if not key:
                    message = message.decode()

                    key = [int(num) for num in message.split(' ')]
                    key = tuple(key)
                    server.send('200'.encode('utf-8'))

                    code_msg = socks.recv(2048)
                    code_msg = code_msg.decode()

                    if ___are_equal(code_msg, 200):
                        server.send(f'{public_key[0]} {public_key[1]}'.encode('utf-8'))

                    msg = socks.recv(2048)
                    msg = msg.decode()
                    print(msg)

                else:
                    message = pickle.loads(message)
                    message = decrypt(message, private_key)
                    print(message)
            else:
                message = sys.stdin.readline()
                encrypted = pickle.dumps(encrypt(message, key))
                server.send(encrypted)

                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()

    except KeyboardInterrupt:
        print('Disconnecting...')
        break

server.close()
