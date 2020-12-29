from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from collegeApp import models
from django.conf import settings
from django.contrib.auth.models import auth
from collegeApp.forms import registerForm
#from blog.models import BlogPost
# Create your views here.
def home(request):
    res=render(request,'collegeApp/homePage.html')
    return res

def register(request):
    if request.method=='POST':
        email=request.POST['email']
        if email[::-1][:6][::-1]=="mit.in":
            password=request.POST['password']
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            links=request.POST['links']
            bio=request.POST['bio']
            role=request.POST['role']
            user=models.User.objects.create_user(email=email,password=password,first_name=first_name,last_name=last_name,links=links,bio=bio,role=role)
            user.save();
            return redirect('collegeApp/login.html')
        else:
            print("Invalid email")
    else:
        return render(request,'collegeApp/registration.html')

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('collegeApp/homePage.html',{'user':user})
        else:
            print("invalid login")
    else:
        return render(request,'collegeApp/login.html')

def editProfile(request):
    user=models.User.objects.get(id=request.GET['uid'])
    fields={'email':user.email,'first_name':user.first_name,'last_name':user.last_name,'links':user.links,'bio':user.bio,'role':user.role}
    form=registerForm(initial=fields)
    res=render(request,'collegeApp/editProfile.html',{'form':form,'user':user})
    return res

def edit(request):
    if request.method=='POST':
        form=registerForm(request.POST)
        #user=models.User()
        #user.id=request.POST['uid']
        user=models.User.objects.get(id=request.POST['uid'])
        user.email=form.data['email']
        #book.price=form.data['price']
        user.first_name=form.data['first_name']
        user.last_name=form.data['last_name']
        user.links=form.data['links']
        user.bio=form.data['bio']
        user.role=form.data['role']
        user.save()
        return HttpResponseRedirect('collegeApp/homePage.html',{'user':user})
