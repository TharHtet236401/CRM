from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, ProfileEditForm
from .models import Record
from .decorators import login_required_with_message
from django.contrib.auth.decorators import login_required
from django.utils.http import quote


# Create your views here.
def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            next_url = request.POST.get('next')
            if next_url:
                return redirect(f'/?next={quote(next_url)}')
            return redirect('home')
    return render(request, 'home.html', {'records': records})

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

@login_required
def customer_record(request, pk):
    try:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record':record})
    except Record.DoesNotExist:
        messages.error(request, "Record does not exist")
        return redirect('home')

@login_required
def delete_record(request, pk):
    try:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, "Record deleted successfully")
        return redirect('home')
    except Record.DoesNotExist:
        messages.error(request, "Record does not exist")
        return redirect('home')

@login_required
def add_record(request):
    try:
        form = AddRecordForm(request.POST or None)
        if request.method == 'POST':
            form.instance.added_by = request.user
            if form.is_valid():
                form.save()
                messages.success(request, "Record added successfully")
                return redirect('home')
        return render(request, 'add_record.html',{'form':form})
    except Exception as e:
        messages.error(request, f"An error occurred while adding record: {str(e)}")
        return redirect('home')

@login_required
def update_record(request, pk):
    try:
        record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Record updated successfully")
                return redirect('home')
        return render(request, 'update_record.html',{'form':form})
    except Record.DoesNotExist:
        messages.error(request, "Record does not exist")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"An error occurred while updating record: {str(e)}")
        return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    try:
        if request.method == 'POST':
            form = ProfileEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('home')
        else:
            form = ProfileEditForm(instance=request.user)
        return render(request, 'edit_profile.html', {'form': form})
    except Exception as e:
        messages.error(request, f"An error occurred while updating profile: {str(e)}")
        return redirect('home')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')



