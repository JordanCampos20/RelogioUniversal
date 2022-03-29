import threading
import socket

#Ip do Computador Server
host = 'localhost'

port = 6666

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    
    for client in clients:
        
        client.send(message)

def handle(client):
    
    while True:
        
        try:
            
            message = client.recv(1024)
            
            broadcast(message)
        
        except:
            
            index = client.index(client)
            
            clients.remove(client)
            
            client.close()
            nickname = nicknames[index]
            
            nicknames.remove(nickname)
            
            break


def receive():
    
    while True:
        client, address = server.accept()
        
        print(f"Conectado pelo IP:{str(address)}")
        
        client.send('NICK'.encode('ascii'))
        
        nickname = client.recv(1024).decode('ascii')
        
        nicknames.append(nickname)
        
        clients.append(client)
        
        thread = threading.Thread(target=handle, args=(client,))
        
        thread.start()


print("Server está Iniciando...")

receive()