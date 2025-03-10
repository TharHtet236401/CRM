from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def login_required_with_message(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to view this page!")
            return redirect('home')
        return function(request, *args, **kwargs)
    return wrap 