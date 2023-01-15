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

def saveService(request):
     if request.method=='POST' :
        userid=request.POST.get('userid')
        user=User.objects.get(id=userid)
        name=request.POST.get('service')
        service=Service()
        service.hospital=Hospital.objects.get(user=user)
        service.name=name
        service.save()

        return redirect('services')

def approveRequest(request):
     if request.method=='POST' :
        requestId=request.POST.get('requestId')
        doctorId=request.POST.get('doctor')
        request1=RequestAppointment.objects.get(id=requestId)
        doctor=Doctor.objects.get(id=doctorId)
        request1.status="approved"
        request1.save()
        date=request.POST.get('date')
        time=request.POST.get('time')
        approvedAppointment=ApprovedAppointment()
        approvedAppointment.date=date
        approvedAppointment.time=time
        approvedAppointment.doctor=doctor
        approvedAppointment.request=request1
        approvedAppointment.save()

        return redirect('requests')



def saveDoctor(request):
     if request.method=='POST' :
        email=request.POST.get('email')
        names=request.POST.get('names')
        tel=request.POST.get('tel')
        userid=request.POST.get('userid')
        user=User.objects.get(id=userid)
        service=request.POST.get('service')
        group = Group.objects.get(name="hospital")
        users = User.objects.create_user(
                                        email=email, password="password@123", username=email)
        users.save()
        users.groups.add(group)
        doctor=Doctor()
        doctor.user=users
        doctor.names=names
        doctor.email=email
        doctor.tel=tel
        doctor.service=Service.objects.get(id=service)
        doctor.hospital=Hospital.objects.get(user=user)
        
        doctor.save()
        




        return redirect('doctors')
        
def dashboard(request):
      appointments= RequestAppointment.objects.all()
      print(appointments)
      return render(request,'site/dashboard/dashboard.html',{"appointments":appointments})

def requests(request):
      appointments= RequestAppointment.objects.all()
      hospital= Hospital.objects.all()
      print(appointments)
      return render(request,'site/dashboard/requests.html',{"appointments":appointments,"hospital":hospital})

def services(request):
      services= Service.objects.all()
      print(services)
      return render(request,'site/dashboard/services.html',{"services":services})      

def doctors(request):
      doctors= Doctor.objects.all()
      services= Service.objects.all()
      print(doctors)
      return render(request,'site/dashboard/doctors.html',{"doctors":doctors,"services":services})      



def getServices(request):
     if request.method=='POST' :
        hospitalId=request.POST.get('hospital')
        hospital=Hospital.objects.get(id=hospitalId)
        service=Service.objects.filter(Q(hospital=hospital))
        print(service)
        return render(request,'site/includes/services.html',{"services":service})

def getSingleRequest(request):
    if request.method=='POST' :
      requestId=request.POST.get('requestId')
      print(requestId+"hello")
      requests= RequestAppointment.objects.get(id=requestId)
      print(requests)
      return render(request,'site/includes/transfer.html',{"requests":requests})

def SingleRequest(request):
    if request.method=='POST' :
      requestId=request.POST.get('requestId')
      requests= RequestAppointment.objects.get(id=requestId)
      doctors= Doctor.objects.filter(Q(service=requests.service))
      return render(request,'site/includes/request.html',{"requests":requests,"doctors":doctors})      

def logoutUser(request):

    logout(request)
    return redirect('')