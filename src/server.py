import socket,threading,pickle

IP_ADDRESS = 'localhost'
PORT = 5000

server = socket.socket()
server.bind((IP_ADDRESS, PORT))
server.listen()

connections = []
send_at_the_beginning = [((0,0,0),True),((255,255,255),False)]

def send_turns():
    while True:
        for client in connections:
            if pickle.loads(client.recv(1024)) == False:
                if client == connections[0]:
                    connections[1].send(pickle.dumps(True))
                elif client == connections[1]:
                    connections[0].send(pickle.dumps(True))

def send_board():
    while True:
        for client in connections:
            if isinstance((temp := pickle.loads(client.recv(2048))),list):
                if client == connections[0]:
                    connections[1].send(pickle.dumps(temp))
                elif client == connections[1]:
                    connections[0].send(pickle.dumps(temp))

def broadcast(entity):
    for client in connections:
        client.send(pickle.dumps(entity))

def handle():
    while True:
        if len(connections) == 2:
            broadcast(True)
            break

        client, addr = server.accept()
        print(f'{addr} connected')
        client.send(pickle.dumps(send_at_the_beginning[len(connections)]))
        connections.append(client)

    send_turn_thread = threading.Thread(target=send_turns)
    send_board_thread = threading.Thread(target=send_board)
    send_turn_thread.start()
    send_board_thread.start()

handle()