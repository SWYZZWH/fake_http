# wait to be fullfilled
from .models import student

def existStudentById(id:int) -> bool:
    return True

def getStudentByName(Name:str) -> list:
    return []

def getStudentById(id:int) ->  student:
    return student(id=1,name ="alice",photo ="NIL")

def getStudentByIdAndName(id:int, name:str) ->  list:
    l = []
    l += getStudentByName(name) 
    s = getStudentById(id)
    if s and s not in l:
        l.append(s)
    return [student(id=1,name ="alice",photo ="photos/alice.png"),student(id=2,name ="tom",photo ="NIL")]

def createStudent(s:student) -> bool:
    return True
    
def deleteStudentById(id:int) -> bool:
    return True