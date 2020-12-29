import socket
import os
import struct
import json


HOST = '127.0.0.1'
PORT = 65439
def upload_image(s):
    while 1:
        filepath = input('please input file path: ')
        print(filepath)
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack(b'128sl', bytes(os.path.basename(filepath), encoding='utf-8'), os.stat(filepath).st_size)
            ##print(os.stat(filepath).st_size)
            s.send(fhead)
            print('client filepath: {0}'.format(filepath))

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print('{0} file send over...'.format(filepath))
                    break
                s.send(data)
        break

def deal_data(conn):
    #print('Accept new connection from {0}'.format(addr))
    #conn.settimeout(500)
    # conn.send(str.encode('Hi, Welcome to the server!'))

    while 1:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.decode().strip('\x00')
            new_filename = os.path.join('./', 'client', fn)
            print('file new name is {0}, filesize if {1}'.format(new_filename,
                                                                 filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print('start receiving...')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print('end receive...')
        # conn.close()
        break

while True:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    i = input("query type:")
    j = input("student id:")
    k = input("student name: ")
    ## type: ADD, Delete, LOOKUP
    a = {'query': i, 'id': j, 'name': k}
    j = json.dumps(a)
    s.send(str.encode(j))
    if a['query'] == "Update" or a['query'] == "Insert":
        upload_image(s)
    data = s.recv(1024).decode()
    print(data)
    if data == b'':
        print("Wrong query format")
    else:
        if json.loads(data) == "404":
            print("Not Found")
        else:
            if json.loads(data) == "200":
                print("good")
        #print(json.loads(data))
            else:
                for row in json.loads(data):
                    #print(row)
                    print("ID = ", row[0])
                    print("NAME = ", row[1])
                    print("PHOTO = ", row[2],'\n')
                    deal_data(s)
    s.close()
