from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps
from urllib.parse import quote

def login_required_with_message(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to view this page!")
            path = request.build_absolute_uri()
            return redirect(f'/?next={quote(path)}')
        return function(request, *args, **kwargs)
    return wrap 