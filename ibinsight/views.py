from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from member.models import *  # Importing CustomUser model from manager app
from manager.models import *

def to_index(request):
    # Redirect to counselor-main page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('to-main')

    # Handling form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            # Check if the user is a counselor
            print("user found !!")
            # Authenticate user
            authenticated_user = authenticate(request, username=username, password=password)
            print("user authenticated")

            # If authentication successful, login user
            if authenticated_user:
                print("user authenticated")
                login(request, authenticated_user)
                print("user logged in")
                return redirect('to-main')
            else:
                messages.error(request, "Invalid login credentials")
                print("Invalid credentials")
                return redirect('to-index')

        except CustomUser.DoesNotExist:
            # Handle non-existing user
            messages.error(request, "User does not exist")
            print("User does not exist")
            return redirect('to-index')

    return render(request, 'index.html', {})

def to_sign_up(request):
    # Handling form submission
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        year_of_graduation = request.POST.get('year_of_graduation')
        password = request.POST.get('password')
        password_confirm = request.POST.get('passwordconfirm')
        major = request.POST.get('major')
        interest = request.POST.get('interest')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('to-sign_up')

        # Check if all required fields are filled
        if not all([username, password, password_confirm, name, year_of_graduation]):
            messages.error(request, "Please fill out all the required fields!")
            return redirect('to-sign_up')

        # Check if password matches confirm password
        if password == password_confirm:
            # Hash password and create new user
            hashed_password = make_password(password)
            new_user = CustomUser(
                username=username,
                name=name,
                year_of_graduation=year_of_graduation,
                password=hashed_password,
                major=major,
                interest=interest,
            )
            new_user.save()
            messages.success(request, "User added successfully!")
            return redirect('to-index')

        else:
            messages.error(request, "Password doesn't match. Please try again!")
            return redirect('to-sign_up')

    return render(request, 'signup.html')

@login_required
def to_main(request):
    if request.method == 'POST':
        major = request.POST.get('major')
        interest = request.POST.get('interest')

        curr_user = request.user

        curr_user.major = major
        curr_user.interest = interest

        curr_user.save()

        return redirect('to-main')

    curr_user = request.user

    context = {
        'curr_user': curr_user,
    }

    return render(request, 'main.html', context)

@login_required
def to_about_ib(request):
    curr_user = request.user

    context = {
        'curr_user': curr_user,
    }
    return render(request, 'aboutib.html', context)

@login_required
def to_about_ib_course_search(request):
    group_list = Group.objects.all()
    course_list = Course.objects.all()

    group_id_list = []
    course_id_list = []
    course_name_list = []
    entry_guidance_list = []
    course_aim_list = []

    for course in course_list:
        group_id_list.append(course.group.id)
        course_id_list.append(course.id)
        course_name_list.append(course.name)
        entry_guidance_list.append(course.entry_guidance)
        course_aim_list.append(course.course_aims)

    curr_user = request.user

    context = {
        'curr_user': curr_user,
        'group_list': group_list,
        'course_list': course_list,
        'course_name_list': course_name_list,
        'group_id_list': group_id_list,
        'course_id_list': course_id_list,
        'entry_guidance_list': entry_guidance_list,
        'course_aim_list': course_aim_list,
    }
    return render(request, 'aboutibcoursesearch.html', context)

# View function for counselor logout
@login_required
def log_out(request):
    logout(request)
    return redirect('to-index')

def to_survey(request):
    if request.method == 'POST':

        nation = request.POST.get('nation')
        major = request.POST.get('major')
        grade = request.POST.get('grade')

        print(nation)
        print(major)
        print(grade)

        return redirect('to-survey')

    return render(request, 'survey.html', {})

