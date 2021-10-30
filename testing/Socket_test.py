# -*- coding: utf-8 -*-
"""
Created on Sep 23 13:00:44 2021

@author: pcochang
"""
#!/usr/bin/env python3

import socket
import time

HOST = ''  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def Lettuce_area(): #sample function for lettuce area computation
    time.sleep(5)
    return 100

def sendtoClient():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((HOST, PORT))
            s.listen()
            print("Successful bind")
        except Exception as e:
            print(e)
            time.sleep(1)

        while True:
            try:
                print("Waiting for connection to accept")
                conn, addr = s.accept()
                break
            except Exception as e:
                print(e)
                time.sleep(1)

        print("Connection accepted")
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print("Received from Client:",data.decode('utf-8'))
                if not data:
                    break
                conn.sendall(str.encode(str(Lettuce_area())))
                
sendtoClient()
