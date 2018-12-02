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

class server:

    def __init__(self):
        self.__localPort = 12000
        self.__remoteIP = '127.0.0.1'
        self.__seqNum = 0
        self.__ackNum = 0
        self.__buffer = ''
        self.__serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        
        self.__state = server_states.CLOSED
        self.__expectedSeq = 0
        self.__recv_buffer_size = 16
        self.__recv_buffer = {}
        self.__sndpkt_buffer_size = 16
        self.__sndpkt_buffer = {}

    def update_state(self, new_state):
        print('\n', self.__state, '->', new_state, '\n')
        self.__state = new_state

    def get_state(self):
        return self.__state

    def bind(self, port=12000):
        self.__serverSocket.bind(('127.0.0.1', self.__localPort))
        
    def rdt_recv(self):                
        print('\n===== rdt receive begin =====')
        pkt, ip = self.__serverSocket.recvfrom(2048)
        recv_pkt = utils.extract_pkt(pkt)
        if recv_pkt.syn == 1:
            return recv_pkt, ip
        if recv_pkt.seqNum == self.__expectedSeq:
            # put packet's data in recv_buffer
            # if buffer is full, then drop
            if len(self.__recv_buffer) < self.__recv_buffer_size:
                self.__recv_buffer[recv_pkt.seqNum] = recv_pkt.data
            pkt = utils.packet()
            pkt.ack = 1
            pkt.ackNum = self.__expectedSeq
            self.rdt_send(pkt, ip)
            self.__expectedSeq = self.__expectedSeq + 1
        else:
            # drop
            pkt = utils.packet()
            pkt.ack = 1
            pkt.ackNum = self.__expectedSeq
            self.rdt_send(pkt, ip)

        print('===== rdt receive end =====\n')
        return recv_pkt, ip
        
    def rdt_send(self, pkt, ip):
        print('\n===== rdt send begin =====')
        sndpkt = pkt.make_pkt()
        self.__serverSocket.sendto(sndpkt, ip)
        print('===== rdt send end =====\n')
    
    def close(self):
        self.__serverSocket.close()


if __name__ == '__main__':
    s = server()
    s.bind(12000)
    while True:
        if s.get_state() == server_states.CLOSED:
            s.update_state(server_states.LISTEN)
        elif s.get_state() == server_states.LISTEN:
            recv_pkt1, remoteIP = s.rdt_recv()
            if recv_pkt1.syn == 1:
                pkt2 = utils.packet()
                # pkt2.seqNum = utils.rand()
                pkt2.ackNum = recv_pkt1.seqNum + 1
                pkt2.ack = 1
                pkt2.syn = 1
                s.rdt_send(pkt2, remoteIP)
                s.update_state(server_states.SYN_RECEIVED)
        elif s.get_state() == server_states.SYN_RECEIVED:
            recv_pkt1, remoteIP = s.rdt_recv()
            if recv_pkt1.ack == 1:
                s.update_state(server_states.ESTABLISHED)
        elif s.get_state() == server_states.ESTABLISHED:
            recv_pkt1, remoteIP = s.rdt_recv()
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
            recv_pkt1, remoteIP = s.rdt_recv()
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
