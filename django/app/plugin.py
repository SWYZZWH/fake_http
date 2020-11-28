# wait to be fullfilled
from .models import student

def existStudentById(id:int) -> bool:
    return True

def getStudentByName(Name:str) -> list:
    return None

def getStudentById(id:int) ->  student:
    return None

def getStudentByIdAndName(id:int, name:str) ->  list:
    l = []
    l += getStudentByName(name)
    s = getStudentById(id)
    if s and s not in l:
        l.append(s)
    return l

def createStudent(s:student) -> bool:
    return True
    
def deleteStudentById(id:int) -> bool:
    return True