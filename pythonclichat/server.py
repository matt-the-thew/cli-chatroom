import socket
import threading
import datetime

HOST = "127.0.0.1"
PORT = 4500

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def generate_timestamp():
    return f"[[{datetime.datetime.now()}]]"


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        finally:
            index = clients.index(clients)
            client.close()
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(
                f"{generate_timestamp()}{nickname.encode('ascii')} left the room."
            )
            nicknames.remove(nickname)


def recieve():
    while True:
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
