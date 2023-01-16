from django.shortcuts import render
from django.http import HttpResponse
from .models import Choice, Question, Notification
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json

def home(request):
    context = {}
    auth = True
    question = Question.objects.all()
    users=User.objects.all()
    if request.user.is_anonymous:
        context = {
            "link":"../login/",
            "text":"Login",
            "question_list":question,
            "users":users
        }   
        return render(request,'index.html',context)
    else:
        context = {
            "link":"../logout/",
            "text":"Logout",
            "question_list":question,
            "users":users.exclude(id = request.user.id)
        }
        return render(request, 'index.html', context)

def create(request):
    if request.user.is_anonymous:
        return redirect('/newpoll/login')
    context = {}
    if request.method == "POST":
        question = Question.objects.create(question=request.POST['question_name'],created_by=request.user)
        Choice.objects.create(question=question,choice_text = request.POST['choice3'],votes = 0)
        Choice.objects.create(question=question,choice_text = request.POST['choice1'],votes = 0)
        Choice.objects.create(question=question,choice_text = request.POST['choice2'],votes = 0)    
        return redirect('/newpoll/home')
    return render(request,'create.html',context)


def register_user(request):
    context = {}
    if request.method=="POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username,email=email,password=password)
        info = Notification.objects.create(userId=user)
        print("success")
        return redirect('/newpoll/home')
    return render(request,'register.html')

def login_user(request):
    if request.user.is_anonymous:
        context = {
            "error":"none",
        }
        if request.method=="POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('/newpoll/home')
            else:
                context = {
                    "error":"Wrong Username or Password",
                }
                return render(request,"login.html",context)
        return render(request,'login.html',context)
    else:
        return redirect('/newpoll/home')


def logout_user(request):
    logout(request)
    return redirect('/newpoll/home')

def view_profile(request):
    if request.user.is_anonymous:
        return redirect('/newpoll/login')
    question = Question.objects.all().filter(created_by=request.user)
    context = {
        "question_list" : question
    }
    return render(request,'profile.html',context)

def vote(request,pk):
    if request.user.is_anonymous:
        return redirect('/newpoll/login')
    # info= Notification.objects.get(userId=request.user)
    # if pk in info.has_voted:
    #     return redirect('/newpoll/result/'+str(pk))
    question = Question.objects.get(id=pk)
    context = {
        "question":question,
    }
    if request.method == "POST":
        # if question in info.noti:
        #     info.noti.remove(question)
        #     info.save()
        # question.vote += 1
        question.save()
        choice_idx = request.POST["choice"]
        choice = Choice.objects.get(id=choice_idx)
        choice.votes += 1
        choice.save()
        return redirect('/newpoll/result/'+str(pk))
    return render(request,'vote.html',context)

def result(request, pk):
    # info = Notification.objects.get(userId=request.user)
    # if pk not in info.has_voted:
    #     info.has_voted.append(pk)
    #     info.save()
    question = Question.objects.get(id=pk)
    choices = Choice.objects.all().filter(question=question)
    choice_list = []
    total = 0
    for cho in choices:
        total = total + cho.votes;
    if total==0:
        total = 1
    for cho in choices:
        choice_list.append(
        {
            "choice":cho,    
            "percen":int(cho.votes/total * 100),
        })
    context = {
        "question":question,
        "choice_list":choice_list,
    }

    return render(request,'result.html',context)

def deletePoll(request,pk):
    question = Question.objects.get(id=pk)
    question.delete()
    return redirect('/newpoll/home')

def sharePoll(request,pk):
    if request.user.is_anonymous:
        return redirect('/newpoll/login')
    question = Question.objects.get(id=pk)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    reciever = body['share']
    user = User.objects.get(id = reciever)
    info = Notification.objects.get(userId=user)
    if question not in info.noti:
        info.noti.append(question)
    info.save()
    print(info.noti)
    return redirect('/newpoll/home')
    # question = Question.objects.get(id=pk)
    # alluser=User.objects.all()
    # context = {
    #     "question":question,
    #     "users":alluser,
    # }
    # return render(request,'share.html',context)

def sharedpoll(request):
    info = Notification.objects.get(userId=request.user)
    context = {
        "question_list":info.noti,
    }
    return render(request,'sharedpoll.html',context)
