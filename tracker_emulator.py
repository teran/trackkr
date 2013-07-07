#!/usr/bin/env python

import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 9000
BUFFER_SIZE = 1024

data = [
    {'title': 'logon', 'message': '##,imei:123456789012345,A;', 'reply': 'LOAD'},
    {'title': 'heartbeat', 'message': '123456789012345;', 'reply': 'ON'},
    {'title': 'tracker no gps', 'message': 'imei:123456789012345,tracker,000000000,+1231234567,L,,,1e4a,,37b0,,,;', 'reply': 'OK'},
    {'title': 'tracker with gps', 'message': 'imei:123456789012345,tracker,1304052202,+1231234567,F,180215.000,A,5545.2352,N,03736.9996,E,0.00,0;', 'reply': 'OK'},
    {'title': 'tracker with gps south latitude', 'message': 'imei:123456789012345,tracker,1304052202,+1231234567,F,180215.000,A,5545.2352,S,03736.9996,E,0.00,0;', 'reply': 'OK'},
    {'title': 'help me no gps', 'message': 'imei:123456789012345,help me,000000000,,L,,,1e4a,,37b0,,,;', 'reply': 'OK'},
    {'title': 'logon', 'message': '##,imei:123456789012377,A;', 'reply': 'LOAD'},
    {'title': 'heartbeat', 'message': '123456789012377;', 'reply': 'ON'},
    {'title': 'tracker no gps', 'message': 'imei:123456789012377,tracker,000000000,+1231234567,L,,,1e4a,,37b0,,,;', 'reply': 'OK'},
    {'title': 'tracker with gps', 'message': 'imei:123456789012377,tracker,1304052202,+1231234567,F,180215.000,A,5545.2352,N,03936.9996,E,0.00,0;', 'reply': 'OK'},
    {'title': 'tracker with gps south latitude', 'message': 'imei:123456789012377,tracker,1304052202,+1231234567,F,180215.000,A,5845.2352,S,03736.9996,E,0.00,0;', 'reply': 'OK'},
    {'title': 'help me no gps', 'message': 'imei:123456789012377,help me,000000000,,L,,,1e4a,,37b0,,,;', 'reply': 'OK'},
    {'title': 'tracker with gps south latitude', 'message': 'imei:123456789012345,tracker,1304052202,+1231234567,F,180215.000,A,5545.2352,N,03736.9996,E,0.00,0;', 'reply': 'OK'},
]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

for i in data:
    s.send(i['message'])
    
    data = s.recv(BUFFER_SIZE).strip()
    if data != i['reply']:
        print "[FAILED] %s: replied '%s', expecting '%s'" % (i['title'], data, i['reply'])
    else:
        print "[  OK  ] %s" % i['title']
    time.sleep(3)
        
time.sleep(5)
s.close()
