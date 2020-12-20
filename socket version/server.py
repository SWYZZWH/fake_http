import socket
import sys
import json
import sqlite3

conn = sqlite3.connect('test.db')

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
    if cursor==[]:
        print("Invalid ID!")
    else:
        for row in cursor:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("PHOTO = ", row[2],'\n')
        cursor = cur.execute("SELECT id, name, photo  from app_student where id ={}".format(id))

    a = json.dumps([i for i in cursor])
    print("updated:")
    conn.close()
    dbAllInfo()
    print("Operation done successfully")
    return a

def dbLookUpByName(name):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cursor = cur.execute("SELECT id, name, photo  from app_student where name ='{}'".format(name))
    if cursor==[]:
        print("Invalid Name!")
    else:
        for row in cursor:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("PHOTO = ", row[2],'\n')
        cursor = cur.execute("SELECT id, name, photo  from app_student where name ='{}'".format(name))

    a = json.dumps([i for i in cursor])
    print("updated:")
    conn.close()
    dbAllInfo()
    print("Operation done successfully")
    return a

def dbInsert(id,name,photo):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cur.execute("INSERT INTO app_student (id, name, photo)  VALUES ({},'{}','{}')".format(id, name, photo))
    conn.commit()
    print("updated:")
    conn.close()
    dbAllInfo()
    print("Operation done successfully")
    return 1

def dbDeleteByID(id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cur.execute("DELETE from app_student where id={}".format(id))
    conn.commit()
    print("updated:")
    conn.close()
    dbAllInfo()
    print("Operation done successfully")
    return 1


def dbUpdateName(id,name):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cur.execute("UPDATE app_student set name = '{}' where id={}".format(name, id))
    conn.commit()
    print("updated:")
    conn.close()
    dbAllInfo()
    print("Operation done successfully")
    return 1

def dbUpdatePhoto(id,photo):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    print("Opened database successfully")
    cur.execute("UPDATE app_student set photo = '{}' where id={}".format(photo, id))
    conn.commit()
    print("updated:")
    conn.close()
    dbAllInfo()
    print("Operation done successfully")
    return 1

def parseQuery(str):
    ##router
    j = json.loads(str)
    try:
        if j['query']=="AllInfo":
            res = dbAllInfo()
        elif j['query']=="LookUpByID":
            res = dbLookUpByID(j["id"])
        elif j['query']=="LookUpByName":
            res = dbLookUpByName(j["Name"])
        elif j['query'] == "Insert":
            res = dbInsert(j["id"],j['name'],j["photo"])
        elif j['query'] == "UpdateName":
            res = dbUpdateName(j["id"],j['name'])
        elif j['query'] == "UpdatePhoto":
            res = dbUpdatePhoto(j["id"], j['photo'])
        elif j["query"] == "DeleteByID":
            res = dbDeleteByID(j["id"])
        else:
            print("Wrong Format")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    return res

HOST = '127.0.0.1'
PORT = 65431
print("Server Started!\n")
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()
while True:
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            print(json.loads(data))
            if not data:
                break
            res = str.encode(parseQuery(data))
            conn.sendall(res)
            break