import mysocket
import threading

server = mysocket.mysocket()
server.bind(('127.0.0.1', 12000))
listen = threading.Thread(target=server.listen, args=(2,))
listen.start()

while True:
    client_sock, client_addr = server.accept()
    data = client_sock.recv(5)
    client_sock.close()
server.close()