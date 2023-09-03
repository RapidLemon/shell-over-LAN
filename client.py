from os import system
import socket

HOST = '192.168.2.11'  # Replace with your server's IP address
PORT = 8000 # Replace with the same port number as the server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

data = client_socket.recv(1024)
print(data.decode(), end="")

while True:
    message = input("\n>>> ")
    if message == "exit":
        break
    elif message == "cls":
        system("cls")
    client_socket.send(message.encode('utf-8'))
    response = client_socket.recv(524288).decode('utf-8')
    print(response[:-2], end="")

client_socket.close()