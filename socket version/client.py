import socket

import json


HOST = '127.0.0.1'
PORT = 8001
while True:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    i = input("query type:")
    j = input("student id:")
    k = input("further info:")
    ## type: ADD, Delete, LOOKUP
    a = {'query': i, 'id': j, 'info': k}
    j = json.dumps(a)
    s.send(str.encode(j))
    data = s.recv(1024)
    if data == b'':
        print("Wrong query format")
    else:
        for row in json.loads(data):
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("PHOTO = ", row[2],'\n')

    s.close()
