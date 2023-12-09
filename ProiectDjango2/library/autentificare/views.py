from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from werkzeug.security import generate_password_hash
from django.contrib.auth import authenticate,login


# Create your views here.

def home(request):
    return render(request,"autentificare/index.html")


def register(request):

    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]
        confirmPassword = request.form["passwordConfirm"]
        if(password == confirmPassword):
            user = User.getByName(name=username)
            if user:
                messages.error(request,"Name already exists")
            else:
                hashed_pass = generate_password_hash(password)
                new_user = User(name=username,password=hashed_pass)

                if new_user:
                    new_user.insertIntoDb()
                    login(request,user=new_user)
                else:
                    messages.error(request,"Error when creating account")


        else:
            messages.error(request,"Try again,the password did not match")
    return render(request,"autentificare/register.html")


def login(request):
    return render(request,"autentificare/login.html")


def logout(request):
    pass
