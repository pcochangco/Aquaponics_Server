# -*- coding: utf-8 -*-
"""
Created on Sep 23 13:00:44 2021

@author: pcochang
"""

import socket

host = ''
port = 1403

data_to_send = "This is a placeholder for lettuce area"

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket for Piserver created")
    try:
        s.bind((host,port))
    except:
        print(socket.error)
    print("Socket bind complete, waiting for connection")
    return s

def setupConnection(s):  
    s.listen(1) #listen to 1 socket at a time
    conn, addr = s.accept()
    print("Now connected to:",addr[0])
    return conn

def dataTransfer(conn):
    try:
        dataFromClient = conn.recv(1024)  # receive data from client
        dataFromClient = dataFromClient.decode('utf-8')
        print("Received request:", dataFromClient)
        
        ######define function here to get the lettuce area
        
        #send back the message(area of lettuce) to the Client
        conn.sendall(str.encode(data_to_send))
    except:
        print("Lost connection, now waiting for connection. . .")
    


while True:
    try:
        s = setupServer()
        conn = setupConnection(s)  #this is where we wait for client request
        dataTransfer(conn)
        s.close()
    except:
        print("The Program encountered an error")
    
