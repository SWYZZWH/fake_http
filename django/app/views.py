from django.contrib.messages.api import success
from django.shortcuts import get_object_or_404, render
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
        print(id,name)

        #id and name can both be None
        # 需要替换为
        students = getStudentByIdAndName(id, name)
        # students = student.objects.all()
        # print(students)
        #         # if id:
        #         #     students = students.filter(id = id)
        #         # print(students)
        #         # if name:
        #         #     students = students.filter(name = name)
        #         # print(students)


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
        # 需要替换为
        #success = deleteStudentById(id)
        success = student.objects.filter(id=id).delete() != None

        if success == True:
            messages.add_message(request, messages.SUCCESS, "删除成功！")
        else:
            messages.add_message(request, messages.ERROR, "删除失败！")
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
    

    success = s_form.is_valid()
    if not success:
        print(s_form.errors)
        messages.add_message(request, messages.ERROR, "表单非法！")
        return redirect("/index")

    name = s_form.cleaned_data["name"]
    photo = s_form.cleaned_data["photo"]

    if id == None or name == None:
        messages.add_message(request, messages.ERROR, "学号或姓名不能为空！")
        return redirect("/index")


    # 需要替换为
    # exsitStudentById(s_form.cleaned_data["id"]):
    is_exist = student.objects.filter(id=s_form.cleaned_data["id"])



    if is_exist:
        messages.add_message(request, messages.ERROR, "不能创建已有的学生！")
        return redirect("/index")


    # 需要替换为
    # createStudent(s_form):
    s_form.save()


    
    messages.add_message(request, messages.INFO, "信息更新成功！")
    return redirect("/index")

####################################################
@csrf_exempt
def update(request, id):
    print(id)
    if id == None:
        messages.add_message(request, messages.ERROR, "学号不能为空！")
        return redirect("/index")

    # 需要替换为
    # s = getStudentById(id)
    s = getStudentById(id)
    print(s)
    #if s is None or s.get("id") != id or s.get("name") == None:
    #    messages.add_message(request, messages.ERROR, "未找到该学生！")
    #    return redirect("/index")

    s_form = StudentForm(initial={"id":s.id, "name":s.name, "photo":s.photo})
    print(request.path)
    return render(request, "info.html", {"form":s_form,"update":True,"base_url":request.path})

@csrf_exempt
def update_submit(request, id):

    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "无效的请求！")
        return redirect("/index")

    
    new_id = int(request.POST.get("id"))
    if new_id != id:
        messages.add_message(request, messages.ERROR, "不能修改ID！")
        return redirect("/index")
    
    # 这个不要换
    student.objects.filter(id=id).delete()

    s_form = StudentForm(request.POST, request.FILES)
    
    success = s_form.is_valid()
    s_form.save()
    # 不是替换，而是添加 save 到远端逻辑
    # success = updateStudent(s_form)

    if not success:
        messages.add_message(request, messages.ERROR, "表单非法！")
        return redirect("/index")

    messages.add_message(request, messages.SUCCESS, "表单合法！")

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
