from django.shortcuts import render,redirect
from django.http import JsonResponse
from datetime import date, datetime, tzinfo
from .models import *
from travelapp.models import * ## importing travelapp models
from django.contrib import messages
import bcrypt
# Create your views here.
def home(request):
    print("Login/Registration Page")
    return render(request,'loginreg.html')

def register(request):
    if request.method=="POST":
        print("Check any errors in the formdata")
        errors=User.objects.reg_validate(request.POST)
        if len(errors)>0:
            print("look like you have errors")
            for key,val in errors.items():
                messages.error(request,val)
            return redirect("/") #### Try to remove this and see what happens
        else:
            print("User Regsitration started ")
            password=request.POST['password']
            pw_hash=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            new_user=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],
            email=request.POST['email'],password=pw_hash)
            request.session['user_id']=new_user.id
            return redirect('/travels')

def login(request):
    if request.method=="POST":
        print("Check any errors from the login form")
        logged_user=User.objects.login_validate(request.POST)
        if logged_user:
            request.session['user_id']=logged_user.id
            return redirect('/travels')
        else:
            messages.error(request,"User name and Password not Matched")
            return redirect("/") #### Try to remove this and see what happens

############## Ajax Functions  ###################
def login_check_ajax(request):
    if request.is_ajax and request.method=="POST":
        print("I am in login_check using ajax")
        print(request.POST.get('email'))
        get_user=User.objects.filter(email=request.POST.get('email'))
        if get_user:
            this_user=get_user[0]
            if bcrypt.checkpw(request.POST.get('password').encode(),this_user.password.encode()):
                request.session['user_id']=this_user.id
                print(this_user.id)
                return JsonResponse('success',safe=False)
        data="Incorrect Email Address and/or Password"
        return JsonResponse(data,safe=False)

def unique_email_check(request):
    if request.is_ajax and request.method=="POST":
        print("I am in unique_email_check ajax")
        print(request.POST.get('email'))
        verify_email=User.objects.filter(email=request.POST.get('email_reg'))
        if not verify_email:
            return JsonResponse('success',safe=False)
        data="This email is already registered"
        return JsonResponse(data,safe=False)