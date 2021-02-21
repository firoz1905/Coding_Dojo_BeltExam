from django.shortcuts import render,redirect
from django.contrib.messages.api import error
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from .models import *
from loginregapp.models import *
# Create your views here.
def travels(request):
    if 'user_id' not in request.session:
        return redirect('/')
    print(request.session['user_id'])
    return render(request,'travels.html',context={
        'logged_user':User.objects.get(id=request.session['user_id']),
        'trips':Trip.objects.all().order_by('-created_at') ### Get the list of trips added by users
    })

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return redirect('/travels')

def addtrip(request):
    if request.method=="GET":
        if 'user_id' not in request.session:
            return redirect('/')
        else:
            logged_user=User.objects.get(id=request.session['user_id'])
            return render(request,'addtrip.html',context={
                'logged_user':logged_user,
            })
    if request.method=="POST":
        print("I am here")
        errors=Trip.objects.trip_validate(request.POST)
        print(errors)
        if len(errors)>0:
            for key,val in errors.items():
                messages.error(request,val)
            return redirect('/travels/addtrip')
        else:
            print("Now i am in Adding a Trip")
            logged_user=User.objects.get(id=request.session['user_id'])
            new_trip=Trip.objects.create(destination=request.POST['destination'],description=request.POST['description'],
            from_date=request.POST['from_date'],to_date=request.POST['to_date'],
            added_by=logged_user)
            print(new_trip)
            logged_user.joined_trips.add(new_trip)
            print(new_trip)
            return redirect('/travels')

def join(request,trip_id):
    if request.method=="GET":
        if 'user_id' not in request.session:
            return redirect('/')
        logged_user=User.objects.get(id=request.session['user_id'])
        print("I am in Join View")
        some_trip=Trip.objects.get(id=trip_id)
        logged_user=User.objects.get(id=request.session['user_id'])
        logged_user.joined_trips.add(some_trip)
        return redirect(f"/travels")

def cancel(request,trip_id):
    if request.method=="GET":
        if 'user_id' not in request.session:
            request.session['user_id']
            return redirect('/')
        logged_user=User.objects.get(id=request.session['user_id'])
        print("I am in cancel View")
        logged_user=User.objects.get(id=request.session['user_id'])
        already_joined_trip=logged_user.joined_trips.get(id=trip_id)
        logged_user.joined_trips.remove(already_joined_trip)
        return redirect(f"/travels")

def delete(request,trip_id):
    if request.method=="GET":
        if 'user_id' not in request.session:
            return redirect('/')
        logged_user=User.objects.get(id=request.session['user_id'])
        trip_to_delete=Trip.objects.get(id=trip_id)
        trip_to_delete.delete()
        return redirect(f"/travels")

def tripview(request,trip_id):
    if request.method=="GET":
        if 'user_id' not in request.session:
            return redirect('/')
        print("I am here to delete")
        logged_user=User.objects.get(id=request.session['user_id'])
        this_trip=Trip.objects.get(id=trip_id)
        return render(request,'tripview.html', context={
            'logged_user':User.objects.get(id=request.session['user_id']),
            'this_trip':Trip.objects.get(id=trip_id),
            'trips':Trip.objects.all(),
            'users':User.objects.all()
            })
def logout(request):
    print("I am here !!")
    request.session.clear()
    return redirect('/')