from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record


# Create your views here.
def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "Login successful")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('home')
    return render(request, 'home.html',{'records':records})

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html',{'form':form})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')



