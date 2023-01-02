from django.shortcuts import render,redirect
from django.contrib.auth import login as loginForm, authenticate,logout
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.db.models import Q
from .models import *

def index(request):
    return render(request,'site/base.html')

def login(request):
    if(request.method=='POST'):
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username+" "+password)
        user = authenticate(username=username,password=password)
        # print(user.is_active)
        if user is not None:
                loginForm(request,user)
                return redirect('dashboard')
        else:
            messages.error(request,'username or password not correct')
            return redirect('login')
    return render(request,'site/login.html')   

def signup(request):
     if request.method=='POST' :
        username=request.POST.get('username')
        name=request.POST.get('name')
        address=request.POST.get('address')
        
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if(password!=cpassword):
            messages.error(request,'password not match')
            return redirect('signup')
        else:

            #  if User.objects.filter(Q(username=username)).exists:
            #     messages.error(request,'User with this username already exist')
            #     return redirect('signup')  
             group = Group.objects.filter(Q(name="patient"))
             if(group.exists):
                patient = Patient()
                group = Group.objects.get(name="patient")
                users = User.objects.create_user(
                                        email=email, password=password, username=username)
                users.save()
                users.groups.add(group)
               
                patient.user=users
                patient.names=name
                patient.address=address
                patient.save()
                messages.error(request,'account created')
                return redirect('login')
             else:
                messages.error(request,'something went wrong')
                return redirect('signup') 
     return render(request, 'site/signup.html')

def signupHospital(request):
     if request.method=='POST' :
        username=request.POST.get('username')
        name=request.POST.get('name')
        address=request.POST.get('address')
        
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if(password!=cpassword):
            messages.error(request,'password not match')
            return redirect('signup')
        else:

            #  if User.objects.filter(Q(username=username)).exists:
            #     messages.error(request,'User with this username already exist')
            #     return redirect('signup')  
             group = Group.objects.filter(Q(name="hospital"))
             if(group.exists):
                hospital = Hospital()
                group = Group.objects.get(name="hospital")
                users = User.objects.create_user(
                                        email=email, password=password, username=username)
                users.save()
                users.groups.add(group)
               
                hospital.user=users
                hospital.name=name
                hospital.address=address
                hospital.save()
                messages.error(request,'account created')
                return redirect('login')
             else:
                messages.error(request,'something went wrong')
                return redirect('signup')   
     return render(request, 'site/signUpHospital.html')    

def saveAppointment(request):
     if request.method=='POST' :
        userid=request.POST.get('userid')
        user=User.objects.get(id=userid)
        service=request.POST.get('service')
        transfer=request.FILES['file']
        
        appointment=RequestAppointment()
        appointment.transfer=transfer
        appointment.service=Service.objects.get(id=service)
        appointment.patient=Patient.objects.get(user=user)
        appointment.status="pending"
        appointment.save()
        




        return redirect('requests')

def dashboard(request):
      appointments= RequestAppointment.objects.all()
      print(appointments)
      return render(request,'site/dashboard/dashboard.html',{"appointments":appointments})

def requests(request):
      appointments= RequestAppointment.objects.all()
      hospital= Hospital.objects.all()
      print(appointments)
      return render(request,'site/dashboard/requests.html',{"appointments":appointments,"hospital":hospital})



def getServices(request):
     if request.method=='POST' :
        hospitalId=request.POST.get('hospital')
        service=Service.objects.filter(Q(id=hospitalId))
        print(service)
        return render(request,'site/includes/services.html',{"services":service})


def logoutUser(request):
    logout(request)
    return redirect('')