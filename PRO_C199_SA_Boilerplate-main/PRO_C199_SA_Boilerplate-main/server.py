import socket
from threading import Thread


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()
print("Waiting for clients...")
list_of_clients = []
nicknames = []

print("Server has started...")

def clientthread(conn, addr):
    conn.send("Welcome to this chatroom!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                print(message)
                broadcast(message, conn)
                #print ("<" + addr[0] + "> " + message)
                #message_to_send = "<" + addr[0] + "> " + message
                #broadcast(message_to_send, conn)
            else:
                remove(conn)
                remove_nickname(nickname)
                
        except:

            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)
        message1 = "{} remove!".format(nickname)
        print(message1)        

while True:
    conn, addr = server.accept()
    conn.send('LETYOURNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    # conn, addr are the client socket object and client ip[ipv4] and port.
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message = "{} joined!".format(nickname)

    print(message)
    broadcast(message, conn)
    #print (addr[0] + " connected")
    new_thread = Thread(target= clientthread,args=(conn,addr))
    new_thread.start()
