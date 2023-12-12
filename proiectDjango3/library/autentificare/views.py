from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, CarteForm
from .models import Carte


# Create your views here.

def home(request):
    if request.user.is_superuser:
        return adminHome(request)
    else:
        return userHome(request)


def adminHome(request):
    if request.method == 'POST':
        form = CarteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Sau redirecționează către o altă pagină după salvare
    else:
        form = CarteForm()

    context = {'form': form}
    return render(request, 'autentificare/home.html', context)


def userHome(request):
    # Logica specifică pentru utilizator normal
    carti = Carte.getCarti()
    context = {'carti': carti}
    return render(request, 'autentificare/home.html', context)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                print("am intrat")
                auth_login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'autentificare/login.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')

            # Autentificarea automată după înregistrare
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            auth_login(request, new_user)

            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'autentificare/register.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


@login_required
def adminView(request):
    if request.user.is_staff:  # Verifică dacă utilizatorul este admin
        return render(request, 'admin_page.html', {'message': 'Logat ca admin'})
    else:
        return HttpResponse("Nu aveți permisiunea să accesați această pagină.")