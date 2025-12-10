import socket
import threading

from public.utils import generate_timestamp

nickname = input("Choose your nickname\n")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 4500))


def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICKNAME":
                client.send(nickname.encode("ascii"))
            else:
                print(f"{generate_timestamp()}::  {message}")
        except:
            client.close()


def write():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode("ascii"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
