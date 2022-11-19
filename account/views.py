from django.shortcuts import render

def index(request):
    return render(request,'site/base.html')

def login(request):
    return render(request,'site/login.html')   


def signUp(request):
    return render(request,'site/signup.html')   

