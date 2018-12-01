# -*- coding: utf-8 -*-

import socket
import utils
from enum import Enum

class client_states(Enum):
    CLOSED=0
    SYN_SENT=1
    ESTABLISHED=2
    FIN_WAIT1=3
    FIN_WAIT2=4
    TIME_WAIT=5

class sender_rdt_states(Enum):
    WAIT_CALL0=0
    WAIT_ACK0=1
    WAIT_CALL1=2
    WAIT_ACK1=3

class client:

    def __init__(self):        
        self.__remoteIP = '127.0.0.1'
        self.__remotePort = 12000
        self.__seqNum = 0
        self.__ackNum = 0
        self.__buffer = ''
        self.__clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__state = client_states.CLOSED

    def connect(self, remoteIP='127.0.0.1', remotePort=12000):
        print('===== handshake begin =====')
        self.__remoteIP = remoteIP
        self.__remotePort = remotePort
        self.__seqNum = utils.rand()

        pkt1 = utils.packet()
        pkt1.seqNum = self.__seqNum
        pkt1.syn = 1
        self.rdt_send(pkt1)
        print('sended: SYN=1, ackNum=0, seqNum=' + str(pkt1.seqNum))
        self.update_state(client_states.SYN_SENT)
        
        if self.get_state() == client_states.SYN_SENT:
            pkt2, remoteIp = self.rdt_recv()
            recv_pkt1 = utils.extract_pkt(pkt2)
            print('received: SYN=' + str(recv_pkt1.syn) + ', ackNum=' + str(recv_pkt1.ackNum) + ', seqNum=' + str(recv_pkt1.seqNum))
            
            if recv_pkt1.ack == 1 and recv_pkt1.ackNum == self.__seqNum + 1 and recv_pkt1.syn == 1 :
                pkt3 = utils.packet()
                pkt3.ackNum = recv_pkt1.seqNum + 1
                pkt3.ack = 1
                self.__seqNum = 0
                self.rdt_send(pkt3)
                print('sended: SYN=0, ackNum=' + str(pkt3.ackNum) + ', seqNum=0')
                self.update_state(client_states.ESTABLISHED)
            else:
                print('syn packet loss')
        
        print('===== handshake end =====')
        
    def close(self):
        print('===== goodbye begin =====')
        while True:
            if self.get_state() == client_states.ESTABLISHED:
                # send fin
                pkt1 = utils.packet()
                # pkt1.seqNum = self.__seqNum
                # todo seqNum check
                pkt1.fin = 1
                self.rdt_send(pkt1)
                print('sended: FIN')
                self.update_state(client_states.FIN_WAIT1)
            elif self.get_state() == client_states.FIN_WAIT1:
                pkt1, remoteIP = self.rdt_recv()
                recv_pkt1 = utils.extract_pkt(pkt1)
                if recv_pkt1.ack == 1: # todo ackNum check                
                    # receive ack and no send
                    print('received: ACK of FIN')
                    self.update_state(client_states.FIN_WAIT2)
            elif self.get_state() == client_states.FIN_WAIT2:
                pkt1, remoteIP = self.rdt_recv()
                recv_pkt1 = utils.extract_pkt(pkt1)
                if recv_pkt1.fin == 1:                
                    # receive fin and send ack
                    print('received: FIN')
                    pkt2 = utils.packet()
                    pkt2.ack = 1
                    self.rdt_send(pkt2)
                    print('sended: ACK of FIN')
                    self.update_state(client_states.TIME_WAIT)
            elif self.get_state() == client_states.TIME_WAIT:
                # wait or not wait
                self.__clientSocket.close()                
                print('closed socket')
                break            
        print('===== goodbye end =====')

    def rdt_send(self, pkt):
        print('===== rdt send begin =====')
        # check state
        pkt.id = 0
        sndpkt = pkt.make_pkt()
        self.__clientSocket.sendto(sndpkt, (self.__remoteIP, self.__remotePort))
        print('===== rdt send end =====')

    def rdt_recv(self):
        print('===== rdt receive begin =====')
        pkt, ip = self.__clientSocket.recvfrom(2048)
        pass
        print('===== rdt receive end =====')
        return pkt, ip

    def update_state(self, new_state):
        print(self.__state, '->', new_state)
        self.__state = new_state

    def get_state(self):
        return self.__state

if __name__ == '__main__':
    c = client()
    c.connect('127.0.0.1', 12000)
    c.close()

# for test
# serverName = '127.0.0.1'
# serverPort = 12000
# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# print('Input lowercase sentence:')

# while True:
#     msg = input('> ')
#     message = bytes(msg, encoding='utf-8')
#     clientSocket.sendto(message, (serverName, serverPort))
#     if msg == 'quit':
#         break
#     modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
#     print(str(modifiedMessage, encoding='utf-8'))

# clientSocket.close()