# -*- coding: utf-8 -*-

import time
import random

class packet:

    def __init__(self):
        self.srcPort = 12000
        self.dstPort = 12000
        self.seqNum = 0
        self.ackNum = 0
        self.ack = 0
        self.syn = 0
        self.fin = 0
        self.id = 0
        self.rwnd = 2048
        self.data = b''

    def __str__(self):
        temp =  'srcPort: ' + str(self.srcPort) + '\n'
        temp += 'dstPort: ' +  str(self.dstPort) + '\n'
        temp += 'seqNum: ' +  str(self.seqNum) + '\n'
        temp += 'ackNum: ' +  str(self.ackNum) + '\n'
        temp += 'ack: ' +  str(self.ack) + '\n'
        temp += 'syn: ' +  str(self.syn) + '\n'
        temp += 'fin: ' +  str(self.fin) + '\n'
        temp += 'id: ' +  str(self.id) + '\n'
        temp += 'rwnd: ' +  str(self.rwnd) + '\n'
        temp += 'data len: ' + str(len(self.data))
        return temp

    def make_pkt(self):
        print('===== make packet begin =====')
        print(self)
        pkt = '{0:016b}'.format(self.srcPort)
        pkt += '{0:016b}'.format(self.dstPort)
        pkt += '{0:032b}'.format(self.seqNum)
        pkt += '{0:032b}'.format(self.ackNum)
        pkt += '{0:01b}'.format(self.ack)
        pkt += '{0:01b}'.format(self.syn)
        pkt += '{0:01b}'.format(self.fin)
        pkt += '{0:01b}'.format(self.id)
        pkt += '{0:016b}'.format(self.rwnd)
        pkt = bytes(pkt, encoding='utf-8')
        if len(self.data) > 0:
            pkt += self.data
        print('===== make packet end =====')
        return pkt

def extract_pkt(pkt):
    print('===== extract packet begin =====')
    # str_pkt = str(pkt, encoding='utf-8')
    # args = str_pkt.split('$')
    bits = str(pkt, encoding='utf-8')
    temp = packet()
    temp.srcPort = int(bits[0:16], 2)
    temp.dstPort = int(bits[16:32], 2)
    temp.seqNum = int(bits[32:64], 2)
    temp.ackNum = int(bits[64:96], 2)
    temp.ack = int(bits[96], 2)
    temp.syn = int(bits[97], 2)
    temp.fin = int(bits[98], 2)
    temp.id = int(bits[99], 2)
    temp.rwnd = int(bits[100:116], 2)
    if len(bits) > 116:
        temp.data = bits[116:]
    print(temp)
    print('===== extract packet end =====')
    return temp

# def udt_send(sock, pkt, ip, port)
#     print('===== udt send begin =====')
#     sock.sendto(pkt, (ip, port))
#     print('===== udt send end =====')

# def udt_recv(sock):
#     print('===== udt receive begin =====')
#     pkt, ip = sock.recvfrom(2048)
#     print('===== udt receive end =====')
#     return pkt, ip

def rand():
    return random.randint(0, 1024)