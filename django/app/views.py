from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import student
from .plugin import *
from .form import *
import logging

@csrf_exempt
def index(request:HttpRequest):
    students = []
    #post request
    if request.method == "POST":
        id = request.POST.get("id", None)
        name = request.POST.get("name", None)

        #id and name can both be None
        students = getStudentByIdAndName(id, name)
        if len(students) == 0:
            messages.add_message(request, messages.ERROR, "未找到学生！")

    return render(request, "index.html", {"students":students, "base_url":request.path})


#####################################################################
@csrf_exempt
def delete(request):
    id = request.GET.get("id", None)
    if id == None or existStudentById(id) == False:
        messages.add_message(request, messages.ERROR, "非法请求！")
    else:
        success = deleteStudentById(id)
        if success == True:
            messages.add_message(request, messages.ERROR, "删除失败！")
        else:
            messages.add_message(request, messages.INFO, "删除成功！")
    return redirect("/index")

##################################################
@csrf_exempt
def create(request):
    #show default photo or uploaded photo
    # photo = request.FILES # only one file
    # if photo:
    #     if photo.get("name") != "photo":
    #         messages.add_message(request, messages.ERROR, "文件名错误！")
    #         return redirect("/index")
    #     return render(request, "info.html", {"photo": photo})
    
    s_form = StudentForm()
    return render(request, "info.html", {"form":s_form, "create":True,"base_url":request.path})

@csrf_exempt
def create_submit(request):
    print("enter")
    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "无效的请求！")
        return redirect("/index")
    
    s_form = StudentForm(request.POST, request.FILES)
    if not s_form.is_valid():
        print(s_form.errors)
        messages.add_message(request, messages.ERROR, "表单非法！")
        return redirect("/index")
        
    s_form.save()
    messages.add_message(request, messages.SUCCESS, "表单合法！")

    id = s_form.cleaned_data["id"]
    name = s_form.cleaned_data["name"]
    photo = s_form.cleaned_data["photo"]

    if id == None or name == None:
        messages.add_message(request, messages.ERROR, "学号或姓名不能为空！")
        return redirect("/index")
    
    # if existStudentById(id):
    #     messages.add_message(request, messages.ERROR, "不能创建已有的学生！")
    #     return redirect("/index")

    # s = student(id, name, photo)
    # try:
    #     createStudent(s)
    # except Exception as e:
    #     messages.add_message(request, messages.ERROR, "信息上传失败！")
    
    
    messages.add_message(request, messages.INFO, "信息更新成功！")
    return redirect("/index")

####################################################
@csrf_exempt
def update(request):
    id = request.GET.get("id")
    if id == None:
        messages.add_message(request, messages.ERROR, "学号不能为空！")
        return redirect("/index")

    s = getStudentById(id)
    if s == None or s.get("id") != id or s.get("name") == None:
        messages.add_message(request, messages.ERROR, "未找到该学生！")
        return redirect("/index")

    s_form = StudentForm(initial={"id":s.id, "name":s.name, "photo":s.photo})
    return render(request, "info.html", {"form":s_form,"update":True,"base_url":request.path})

@csrf_exempt
def update_submit(request):
    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "无效的请求！")
        return redirect("/index")



    s_form = StudentForm(request.POST, request.FILES)
    if not s_form.is_valid():
        messages.add_message(request, messages.ERROR, "表单非法！")
        return redirect("/index")
        
    s_form.save()
    messages.add_message(request, messages.SUCCESS, "表单合法！")

    id = s_form.cleaned_data["id"]
    name = s_form.cleaned_data["name"]
    photo = s_form.cleaned_data["photo"]

    if id == None or name == None:
        messages.add_message(request, messages.ERROR, "学号或姓名不能为空！")
        return redirect("/index")
    
    if id != request.GET.get("id", None):
        messages.add_message(request, messages.ERROR, "学号不能修改！")
        return redirect("/index")

    s = student(id, name, photo)

    # try:
    #     s = student(id, name, photo) 
    # except Exception as e:
    #     messages.add_message(request, messages.ERROR, "图片错误！")
    #     return redirect("/index")

    #double try-catch block, ensure atomic operation
    # try:
    #     original_s = getStudentById(id)
    #     deleteStudentById(s.get("id"))
    #     try:
    #         createStudent(s)
    #     except Exception as e:
    #         messages.add_message(request, messages.ERROR, "信息上传失败！")
    #         createStudent(original_s)
    # except Exception as e:
    #     messages.add_message(request, messages.ERROR, "信息上传失败！")
    #     return redirect("/index")
    
    messages.add_message(request, messages.INFO, "信息更新成功！")
    return redirect("/index")

####################################################
@csrf_exempt
def upload(request):
    if request.FILES == None:
        messages.add_message(request, messages.INFO, "图片为空！")

    if "update" in request.path:
        return redirect("update")
    elif "create" in request.path:
        return redirect("create")
    else:
        messages.add_message(request, messages.ERROR, "上传错误，url非法！")
        return redirect("/index")
