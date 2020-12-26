# wait to be fullfilled
from .models import student
from .form import StudentForm

def existStudentById(id:int) -> bool:
    return True

def getStudentByName(Name:str) -> list:
    return []

def getStudentById(id:int) ->  student:
    return None

def getStudentByIdAndName(id:int, name:str) ->  list:
    l = []
    l += getStudentByName(name) 
    s = getStudentById(id)
    if s and s not in l:
        l.append(s)
    return l

def createStudent(s_form:StudentForm) -> bool:
    id = s_form.cleaned_data["id"]
    name = s_form.cleaned_data["name"]
    photo = s_form.cleaned_data["photo"]

    return True

def updateStudent(s_form:StudentForm) -> bool:
    id = s_form.cleaned_data["id"]
    name = s_form.cleaned_data["name"]
    photo = s_form.cleaned_data["photo"]
    
    return True
    
def deleteStudentById(id:int) -> bool:
    return True