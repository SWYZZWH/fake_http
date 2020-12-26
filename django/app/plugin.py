# wait to be fullfilled
from .models import student
from .form import StudentForm
from django.core.files import File

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
    return True

def getStudentByName(Name:str) -> list:
    # use createStudentFromFiledir(id, name, filedir) to create student
    return []

def getStudentById(id:int) ->  student:
    # use createStudentFromFiledir(id, name, filedir) to create student
    return student(id=1,name ="alice",photo ="NIL")

def getStudentByIdAndName(id:int, name:str) ->  list:
    l = []
    l += getStudentByName(name) 
    s = getStudentById(id)
    if s and s not in l:
        l.append(s)

    # use createStudentFromFiledir(id, name, filedir) to create student
    return [student(id=1,name ="alice",photo ="photos/alice.png"),student(id=2,name ="tom",photo ="NIL")]

def createStudent(s_form:StudentForm) -> bool:
    id = s_form.cleaned_data["id"]
    name = s_form.cleaned_data["name"]
    photodir = getFiledirFromStudentForm(s_form)

    return True

def updateStudent(s_form:StudentForm) -> bool:
    id = s_form.cleaned_data["id"]
    name = s_form.cleaned_data["name"]
    photodir = getFiledirFromStudentForm(s_form)
    
    return True
    
def deleteStudentById(id:int) -> bool:
    return True