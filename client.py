# -*- coding: utf-8 -*-

import socket
import utils
from enum import Enum
import multiprocessing
import threading

class client_states(Enum):
    CLOSED=0
    SYN_SENT=1
    ESTABLISHED=2
    FIN_WAIT1=3
    FIN_WAIT2=4
    TIME_WAIT=5

class client:

    def __init__(self):        
        self.__remoteIP = '127.0.0.1'
        self.__remotePort = 12000
        self.__seqNum = 0
        self.__ackNum = 0
        self.__rcvpkt_buffer_size = 2048
        self.__rcvpkt_buffer = {}
        self.__clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__clientSocket.settimeout(2)
        self.__state = client_states.CLOSED
        self.__base = 0
        # self.__seqNum = 0
        self.__sndpkt_buffer_size = 8
        self.__sndpkt_buffer = {}
        self.__MSS = 1024

    def connect(self, remoteIP='127.0.0.1', remotePort=12000):
        print('===== handshake begin =====')
        self.__remoteIP = remoteIP
        self.__remotePort = remotePort
        # self.__seqNum = utils.rand()

        while True:
            if self.get_state() == client_states.CLOSED:
                pkt1 = utils.packet()
                pkt1.seqNum = self.__seqNum
                pkt1.syn = 1
                self.rdt_send(pkt1)
                print('sended: SYN=1, ackNum=0, seqNum=' + str(pkt1.seqNum))
                self.update_state(client_states.SYN_SENT)
            elif self.get_state() == client_states.SYN_SENT:
                recv_pkt1, remoteIp = self.rdt_recv()
                print('received: SYN=' + str(recv_pkt1.syn) + ', ackNum=' + str(recv_pkt1.ackNum) + ', seqNum=' + str(recv_pkt1.seqNum))
                
                if recv_pkt1.ack == 1 and recv_pkt1.ackNum == self.__seqNum and recv_pkt1.syn == 1 :
                    pkt3 = utils.packet()
                    pkt3.ackNum = recv_pkt1.seqNum + 1
                    pkt3.ack = 1
                    self.__seqNum = 0   # reset seqNum
                    self.rdt_send(pkt3)
                    print('sended: SYN=0, ackNum=' + str(pkt3.ackNum) + ', seqNum=0')
                    self.update_state(client_states.ESTABLISHED)
                    break
        
        print('===== handshake end =====\n')
        
    def close(self):
        print('===== goodbye begin =====')
        self.__sndpkt_buffer.clear()
        while True:
            if self.get_state() == client_states.ESTABLISHED:
                # send fin
                pkt1 = utils.packet()
                # pkt1.seqNum = self.__seqNum + 1
                # todo seqNum check
                pkt1.fin = 1
                self.rdt_send(pkt1)
                print('sended: FIN')
                self.update_state(client_states.FIN_WAIT1)
            elif self.get_state() == client_states.FIN_WAIT1:
                recv_pkt1, remoteIP = self.rdt_recv()
                if recv_pkt1.ack == 1: # todo ackNum check                
                    # receive ack and no send
                    print('received: ACK of FIN')
                    self.update_state(client_states.FIN_WAIT2)
            elif self.get_state() == client_states.FIN_WAIT2:
                recv_pkt1, remoteIP = self.rdt_recv()
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
                self.update_state(client_states.CLOSED)
                break            
        print('===== goodbye end =====\n')

    def rdt_send(self, pkt):          
        print('send buffer used:', len(self.__sndpkt_buffer), '(before send)')
        if self.__seqNum < self.__base + self.__sndpkt_buffer_size:            
            print('\n===== rdt send begin =====')
            pkt.seqNum = self.__seqNum
            self.__sndpkt_buffer[self.__seqNum] = pkt.make_pkt()
            self.__clientSocket.sendto(self.__sndpkt_buffer[self.__seqNum], (self.__remoteIP, self.__remotePort))
            if self.__base == self.__seqNum:
                # start_timer()
                pass
            self.__seqNum += 1
            print('===== rdt send end =====\n')
            return True
        else:
            # refuse_data()
            print('can not send yet')
            pass
            return False     

    def send(self, data):
        n = int(len(data) / (self.__MSS * 8))
        if n > self.__sndpkt_buffer_size:
            print('data too long, please make it smaller and resend')
            return False
        for i in range(n - 1):
            pkt1 = utils.packet()
            pkt1.seqNum = self.__seqNum            
            pkt1.data = data[i*self.__MSS : (i+1)*self.__MSS]
            self.rdt_send(pkt1)
        pkt1 = utils.packet()
        pkt1.seqNum = self.__seqNum
        pkt1.data = data[(n-1)*self.__MSS:]
        self.rdt_send(pkt1)

        count = 3 # max resend times
        while True:
            try:
                recv_pkt, ip = self.rdt_recv()
                self.__base = recv_pkt.ackNum + 1
                if self.__base == self.__seqNum:                                        
                    self.__sndpkt_buffer.clear()
                    break
            except:
                # receive timeout: resend
                for i in range(self.__base, self.__seqNum):
                    # resend the packet not ack
                    self.__clientSocket.sendto(self.__sndpkt_buffer[i], (self.__remoteIP, self.__remotePort))
                count -= 1
                if count < 0:
                    return False               
        return True

    def rdt_recv(self):
        print('\n===== rdt receive begin =====')
        pkt, ip = self.__clientSocket.recvfrom(2048)        
        recv_pkt = utils.extract_pkt(pkt)
        print('===== rdt receive end =====\n')
        return recv_pkt, ip

    def update_state(self, new_state):
        print('\n', self.__state, '->', new_state, '\n')
        self.__state = new_state

    def get_state(self):
        return self.__state

if __name__ == '__main__':
    c = client()
    c.connect('127.0.0.1', 12000)
    for i in range(3):
        data = bytes(str(i), encoding='utf-8')
        c.send(data)
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