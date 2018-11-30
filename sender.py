# -*- coding: utf-8 -*-

import socket

# for test
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('Input lowercase sentence:')

while True:
    msg = input('> ')
    message = bytes(msg, encoding='utf-8')
    clientSocket.sendto(message, (serverName, serverPort))
    if msg == 'quit':
        break
    modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
    print(str(modifiedMessage, encoding='utf-8'))

clientSocket.close()