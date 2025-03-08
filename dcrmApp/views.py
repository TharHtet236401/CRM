from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request, 'home.html',{})

def register(request):
    pass

def login(request):
    pass

def logout(request):
    pass



