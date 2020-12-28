import socket
import sys
import json
import sqlite3
from threading import Thread
import time
import threading
import struct
import os

def child_connection(index, sock, connection):
    try:
        print("begin connecion ", index)
        print("begin connecion %d" % index)
        # 获得一个连接，然后开始循环处理这个连接发送的信息
        while True:
            buf = connection.recv(1024)
            print("Get value %s from connection %d: " % (buf, index))
            if buf == '1':
                print("send welcome")

                connection.send('welcome to server!')
            elif buf != '0':
                connection.send('please go out!')
                print("send refuse")

            else:
                print("close")

                break  # 退出连接监听循环
    except socket.timeout:  # 如果建立连接后，该连接在设定的时间内无数据发来，则time out
        print('time out')


# def parseQuery(str):
#     print(str.split())
#     if len(str.split())==3:
#         return True
#     else:
#         return "F"
def dbAllInfo():
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cursor = cur.execute("SELECT id, name, photo  from app_student")
    for row in cursor:
        print("ID = ", row[0])
        print("NAME = ", row[1])
        print("PHOTO = ", row[2],'\n')
    cursor = cur.execute("SELECT id, name, photo  from app_student")
    a = json.dumps([i for i in cursor])
    conn.close()
    print("Operation done successfully")
    return a

def dbLookUpByID(id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cursor = cur.execute("SELECT id, name, photo  from app_student where id ={}".format(id))
    if [i for i in cursor] == []:
        a = json.dumps("404")
        print("Invalid ID!")
    else:
        for row in cursor:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("PHOTO = ", row[2],'\n')
        cursor = cur.execute("SELECT id, name, photo  from app_student where id ={}".format(id))
        a = json.dumps([i for i in cursor])
    conn.close()
    print("Operation done successfully")
    return a

def dbLookUpByName(name):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cursor = cur.execute("SELECT id, name, photo  from app_student where name ='{}'".format(name))
    if [i for i in cursor] == []:
        a = json.dumps("404")
        print("Invalid Name!")
    else:
        for row in cursor:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("PHOTO = ", row[2],'\n')
        cursor = cur.execute("SELECT id, name, photo  from app_student where name ='{}'".format(name))
        a = json.dumps([i for i in cursor])

    conn.close()
    print("Operation done successfully")
    return True,a

def dbInsert(id,name,client,address):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cur.execute("INSERT INTO app_student (id, name, photo)  VALUES ({},'{}','{}')".format(id, name, "{}.png".format(id)))
    conn.commit()
    deal_data(client, address,"{}.png".format(id))
    print("updated:")
    a = dbLookUpByID(id)
    print(a)
    conn.close()
    print("Operation done successfully")
    return True,a

def dbDeleteByID(id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cur.execute("DELETE from app_student where id={}".format(id))
    conn.commit()
    print("updated:")
    a = dbAllInfo()
    conn.close()
    print("Operation done successfully")
    return True,a


def dbUpdateName(id,name):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cur.execute("UPDATE app_student set name = '{}' where id={}".format(name, id))
    conn.commit()
    a=dbLookUpByID(id)
    print("updated:")
    print(a)
    conn.close()
    print("Operation done successfully")
    return True,a

def dbUpdate(id,name,client,address):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cur.execute("UPDATE app_student set photo = '{}' where id={}".format("{}.png".format(id), id))
    cur.execute("UPDATE app_student set name = '{}' where id={}".format(name, id))
    conn.commit()
    deal_data(client, address,"{}.png".format(id))
    print("updated:")
    a=dbLookUpByID(id)
    print(a)
    conn.close()
    print("Operation done successfully")
    return "True",a

def parseQuery(str,client,address):
    ##router
    j = json.loads(str)
    try:
        if j['query']=="AllInfo":
            res = dbAllInfo()
        elif j['query']=="LookUpByID":
            res = dbLookUpByID(j["id"])
        elif j['query']=="LookUpByName":
            _,res = dbLookUpByName(j["name"])
        elif j['query'] == "Insert":
            _,res = dbInsert(j["id"],j['name'],client,address)
        elif j['query'] == "UpdateName":
            _,res = dbUpdateName(j["id"],j['name'])
        elif j['query'] == "Update":
            _,res = dbUpdate(j["id"], j['name'],client,address)
        elif j["query"] == "DeleteByID":
            _,res = dbDeleteByID(j["id"])
        else:
            print("Wrong Format")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    return res

# HOST = '127.0.0.1'
# PORT = 8002
# print("Server is starting")
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind((HOST, PORT))  # 配置soket，绑定IP地址和端口号
# sock.listen(5)  # 设置最大允许连接数，各连接和server的通信遵循FIFO原则
# print( "Server is listenting port 8001, with max connection 5")
#
# index = 0
# while True:  # 循环轮询socket状态，等待访问
#     connection, address = sock.accept()
#     index += 1
#     # 当获取一个新连接时，启动一个新线程来处理这个连接
#     _thread.start_new_thread(child_connection, (index, sock, connection))
#     if index > 10:
#         break
#     sock.close()

g_conn_pool = {}  # 连接池
g_socket_server = None  # 负责监听的socket

def init():
    HOST = '127.0.0.1'
    PORT = 65434
    print("Server is starting")
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))  # 配置soket，绑定IP地址和端口号
    sock.listen(5)  # 设置最大允许连接数，各连接和server的通信遵循FIFO原则
    print( "Server is listenting port {}, with max connection 5".format(PORT))

def message_handle(client, info):
    """
    消息处理
    """
    while True:
        data = client.recv(1024)
        print(json.loads(data))
        if not data:
            break
        data = parseQuery(data,client,info)
        res = str.encode(data)
        client.sendall(res)
        if json.loads(data) != "404":
            for row in json.loads(data):
                #print(row)
                print("ID = ", row[0])
                print("NAME = ", row[1])
                print("PHOTO = ", row[2],'\n')
                new_filename = os.path.join('./', 'server',row[2])
                print(new_filename)
                upload_image(client, new_filename)
        break

def accept_client():
    """
    接收新连接
    """
    while True:
        client, info = sock.accept()  # 阻塞，等待客户端连接
        # 给每个客户端创建一个独立的线程进行管理
        print("Connected by", info)
        thread = Thread(target=message_handle, args=(client, info))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()


def remove_client(client_type):
    client = g_conn_pool[client_type]
    if None != client:
        client.close()
        g_conn_pool.pop(client_type)
        print("client offline: " + client_type)

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 6666))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr,new_file):
    print('Accept new connection from {0}'.format(addr))
    #conn.settimeout(500)
    # conn.send(str.encode('Hi, Welcome to the server!'))

    while 1:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.decode().strip('\x00')
            new_filename = os.path.join('./', 'server/' + new_file)
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

def upload_image(s,filepath):
    while 1:
        print(filepath)
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack(b'128sl', bytes(os.path.basename(filepath), encoding='utf-8'), os.stat(filepath).st_size)
            print(os.stat(filepath).st_size)
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



if __name__ == '__main__':
    init()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    # 主线程逻辑
    while True:
        time.sleep(0.1)