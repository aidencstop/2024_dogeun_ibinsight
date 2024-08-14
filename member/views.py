from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template

from .models import *  # Importing models from current app


# Create your views here.
def member_login(request):
    # Redirect to student-main page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('member-main')

    # Handling form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            authenticated_user = authenticate(request, username=username, password=password)
            print("user authenticated")

            # If authentication successful, login user
            if authenticated_user:
                print("user authenticated")
                login(request, authenticated_user)
                print("user logged in")
                return redirect('member-main')
            else:
                messages.error(request, "Invalid login credentials")
                print("Invalid credentials")
                return redirect('member-login')


        except CustomUser.DoesNotExist:
            # Handle non-existing user
            messages.error(request, "User does not exist")
            print("User does not exist")
            return redirect('member-login')

    # Render login page if request method is GET
    return render(request, 'home.html', {})
