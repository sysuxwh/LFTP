# -*- coding: utf-8 -*-

import socket
import utils
from enum import Enum
import numpy as np

class server_states(Enum):
    CLOSED=0
    LISTEN=1
    SYN_RECEIVED=2
    ESTABLISHED=3
    CLOSED_WAIT=4
    LAST_ACK=5

class receiver_rdt_states(Enum):
    WAIT_RECV0=0
    WAIT_RECV1=1

class server:

    def __init__(self):
        self.__localPort = range(12000, 13000)
        self.__usedPort = np.zeros(1000)
        self.__remoteIP = '127.0.0.1'
        self.__remotePort = 12000
        self.__seqNum = 0
        self.__ackNum = 0
        self.__buffer = ''
        self.__serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__serverSocket.bind(('127.0.0.1', self.__localPort[0]))
        self.__state = server_states.CLOSED

    def update_state(self, new_state):
        print(self.__state, '->', new_state)
        self.__state = new_state

    def get_state(self):
        return self.__state

    def rdt_recv(self):
        print('===== rdt receive begin =====')
        pkt, ip = self.__serverSocket.recvfrom(2048)
        pass
        print('===== rdt receive end =====')
        return pkt, ip
        
    def rdt_send(self, pkt, ip):
        print('===== rdt send begin =====')
        # check state
        pkt.id = 0
        sndpkt = pkt.make_pkt()
        self.__serverSocket.sendto(sndpkt, ip)
        print('===== rdt send end =====')
    
    def close(self):
        self.__serverSocket.close()


if __name__ == '__main__':
    s = server()
    while True:
        if s.get_state() == server_states.CLOSED:
            s.update_state(server_states.LISTEN)
        elif s.get_state() == server_states.LISTEN:
            pkt1, remoteIP = s.rdt_recv()
            recv_pkt1 = utils.extract_pkt(pkt1)
            if recv_pkt1.syn == 1:
                pkt2 = utils.packet()
                pkt2.seqNum = utils.rand()
                pkt2.ackNum = recv_pkt1.seqNum + 1
                pkt2.ack = 1
                pkt2.syn = 1
                s.rdt_send(pkt2, remoteIP)
                s.update_state(server_states.SYN_RECEIVED)
        elif s.get_state() == server_states.SYN_RECEIVED:
            pkt1, remoteIP = s.rdt_recv()
            recv_pkt1 = utils.extract_pkt(pkt1)
            if recv_pkt1.ack == 1:
                s.update_state(server_states.ESTABLISHED)
        elif s.get_state() == server_states.ESTABLISHED:
            pkt1, remoteIP = s.rdt_recv()
            recv_pkt1 = utils.extract_pkt(pkt1)
            if recv_pkt1.fin == 1:
                # receive fin and send ack
                pkt2 = utils.packet()
                # set seqNum and ackNum?
                pkt2.ack = 1
                s.rdt_send(pkt2, remoteIP)
                s.update_state(server_states.CLOSED_WAIT)
            elif False:
                pass
        elif s.get_state() == server_states.CLOSED_WAIT:
            # if is ready to close
            pkt2 = utils.packet()
            # set seqNum and ackNum?
            pkt2.fin = 1
            s.rdt_send(pkt2, remoteIP)
            s.update_state(server_states.LAST_ACK)
        elif s.get_state() == server_states.LAST_ACK:
            pkt1, remoteIP = s.rdt_recv()
            recv_pkt1 = utils.extract_pkt(pkt1)
            if recv_pkt1.ack == 1:
                # receive ack and no send
                s.update_state(server_states.CLOSED)
                break
    s.close()
    print('closed socket')
    
# for test
# serverPort = 12000
# serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# serverSocket.bind(('127.0.0.1', serverPort))
# print("The server is ready to receive")

# while True:
#     message, clientAddress = serverSocket.recvfrom(2048)
#     msg = str(message, encoding='utf-8')
#     print('Server received: ' + msg)
#     if (msg == 'quit'):
#         break
#     modifiedMessage = message.upper()
#     serverSocket.sendto(modifiedMessage, clientAddress)

# serverSocket.close()
