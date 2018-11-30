# -*- coding: utf-8 -*-

import socket

# for test
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('127.0.0.1', serverPort))
print("The server is ready to receive")

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    msg = str(message, encoding='utf-8')
    print('Server received: ' + msg)
    if (msg == 'quit'):
        break
    modifiedMessage = message.upper()
    serverSocket.sendto(modifiedMessage, clientAddress)

serverSocket.close()
