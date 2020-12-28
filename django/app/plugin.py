# wait to be fullfilled
from .models import student
from .form import StudentForm
from django.core.files import File
import socket
import os
import struct
import json


HOST = '127.0.0.1'
PORT = 65434

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
            new_filename = os.path.join(os.getcwd(), 'media', fn)
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


def transferFile2Django(filedir):
    return File(open(filedir,"rb"))

def createStudentFromFiledir(id, name, filedir) -> student:
    return student(id, name, transferFile2Django(filedir))

def getFiledirFromStudentForm(s_form:StudentForm) -> str:
    photo = s_form.cleaned_data["photo"]
    return photo.path

def getFiledirFromStudent(s:student) -> str:
    photo = s.photo
    return photo.path

def existStudentById(id:int) -> bool:
    print("getStudentById", id)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    i = "LookUpByID"
    k = id
    ## type: ADD, Delete, LOOKUP
    a = {'query': i, 'id': k}
    print(a)
    j = json.dumps(a)
    s.send(str.encode(j))
    data = s.recv(1024).decode()
    s.close()
    if data == b'':
        print("Wrong query format")
        return False
    else:
        if json.loads(data) == "404":
            return False
        else:
            return True
    # use createStudentFromFiledir(id, name, filedir) to create student

def getStudentByName(Name:str) -> list:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    i = "LookUpByName"
    k = Name
    ## type: ADD, Delete, LOOKUP
    a = {'query': i, 'name': k}
    j = json.dumps(a)
    s.send(str.encode(j))
    data = s.recv(1024).decode()
    stu_list=[]
    if data == b'':
        print("Wrong query format")
        if json.loads(data) == "404":
            print("Not Found")
        else:
            # print(json.loads(data))
            stu_list = []
            for row in json.loads(data):
                # print(row)
                print("ID = ", row[0])
                print("NAME = ", row[1])
                print("PHOTO = ", row[2], '\n')
                deal_data(s)
                stu_list.append(student(id=row[0],name =row[1],photo =row[2]))
    s.close()

    # use createStudentFromFiledir(id, name, filedir) to create student
    return stu_list

def getStudentById(id:int) ->  student:
    print("getStudentById", id)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    i = "LookUpByID"
    k = id
    ## type: ADD, Delete, LOOKUP
    a = {'query': i, 'id': k}
    print(a)
    j = json.dumps(a)
    s.send(str.encode(j))
    data = s.recv(1024).decode()
    if data == b'':
        print("Wrong query format")
    else:
        if json.loads(data) == "404":
            print("Not Found")
        else:
        #print(json.loads(data))
            for row in json.loads(data):
                #print(row)
                print("ID = ", row[0])
                print("NAME = ", row[1])
                print("PHOTO = ", row[2],'\n')
                deal_data(s)
    s.close()
    # use createStudentFromFiledir(id, name, filedir) to create student

    return student(id=row[0],name =row[1],photo =row[2])

def getStudentByIdAndName(id:int, name:str) ->  list:
    l=getStudentByName(name)
    print("getStudentByIdAndName",id,name)
    s = getStudentById(id)
    if s and s not in l:
        l.append(s)
    # use createStudentFromFiledir(id, name, filedir) to create student
    return l

def createStudent(s_form:StudentForm) -> bool:
    id = s_form.cleaned_data["id"]
    name = s_form.cleaned_data["name"]
    photodir = getFiledirFromStudentForm(s_form)

    return True

def updateStudent(s_form:StudentForm) -> bool:
    id = s_form.initial["id"]
    name = s_form.cleaned_data["name"]
    photodir = getFiledirFromStudentForm(s_form)
    print(id,name,photodir)

    return True
    
def deleteStudentById(id:int) -> bool:
    return True