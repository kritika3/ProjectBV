from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django import forms

from . import pycode
from . forms import RegistrationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib import auth

from .pycode import output_function

'''
1. Registration Page ---->> Save name and mail id in Database
2. if registered already --->> click login ---->> Login Page ---->> confirm the details from DB
3. After successful login ---->> Login Button click ---->> Home Page
4. Home Page :  
        -->> RUN button ---->>  click RUN button ----->>> Video starts playing, i.e, ---->> redirect
            to .py file
Flow if the user is registered:

Login Page --->> Enter name and email id --->> Submit:
                                                    if entered detials are correct:
                                                    ----->>> Redirect to Home Page
                                                    else:
                                                    --->>>> Redirect to Login Page

Home Page ------>>>> Click PLAY Button --->> Redirect to main_code.py file

'''
# def current_datetime(request):
#     now = datetime.datetime.now()
#     html = "<html><body>It is now %s.</body></html>" % now
#     return HttpResponse(html)
# def send_message(email, pas):
#     print(email + pas)
def first_page(request):
    return render(request, 'django_app/index.html')

#----------Registration Page------------
def registration_page(request):
    if request.method == 'POST':
        form1 = RegistrationForm(request.POST)
        if form1.is_valid():
            username = form1.cleaned_data['username']
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            User.objects.create_user(username= username, first_name= first_name, last_name= last_name, password=password )
            return HttpResponseRedirect('/login/')
    else:
        form1 = RegistrationForm()
    return render(request, 'django_app/registration.html', {'form': form1})

#---------  Login Page ---------------
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        try:
            user = auth.authenticate(username= username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                messages.error(request, "Email or Password incorrect")
        except ObjectDoesNotExist:
            print("Invalid user")
    return render(request, 'django_app/login.html')


#---------Home Page-----------
def home_page(request):
    return render(request, 'django_app/home.html')

def video_play(request):
    print("Hello! the python code is being executed.")
    s = output_function()
    return render(request, 'django_app/home.html', {'string': s} )