import socket
import threading
from public.utils import generate_timestamp, is_not_ascii

HOST = "127.0.0.1"
PORT = 4500

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    message = message
    if is_not_ascii(message):
        message = message.encode("ascii")
    for client in clients:
        client.send(f"{generate_timestamp()}:: {message}".encode("ascii"))


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            client.close()
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(
                f"{generate_timestamp()}{nickname.encode('ascii')} left the room."
            )
            nicknames.remove(nickname)
            break


def recieve():
    while True:
        print(f"{generate_timestamp()}Server listening on port {PORT}")
        client, address = server.accept()
        print(f"{generate_timestamp()}Connected to {str(address)}")
        client.send("NICKNAME".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)
        print(f"{generate_timestamp()}Nickname is {nickname}")
        broadcast(f"{generate_timestamp()}{nickname} joined!")
        client.send(f"{generate_timestamp()}Connected to server.".encode("ascii"))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


recieve()
