from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserLoginForm, CarteForm
from .models import Carte, UserProfile


# Create your views here.
@login_required()
def home(request):
    if request.user.is_superuser:
        return adminHome(request)
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.approved:
            return userHome(request)
        else:
            return render(request, 'autentificare/pending_page.html')


def adminHome(request):
    if request.method == 'POST':
        form = CarteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CarteForm()

    query = request.GET.get('search_query')
    if query:
        carti_cautate = Carte.getCarteByTitle(titlu=query)
    else:
        carti_cautate = None
    print("CARTI CAUTATEEEE")

    context = {'form': form, 'carti_cautate': carti_cautate}

    return render(request, 'autentificare/home.html', context)


def userHome(request):
    carti_disponibile = Carte.objects.filter(disponibil=True)
    context = {'carti_disponibile': carti_disponibile}
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
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.approved:
                    return redirect('home')
                else:
                    messages.error(request, 'Your account is pending approval.')  # Mesaj pentru utilizatorul neaprobat
                    return render(request, 'autentificare/pending_page.html')
    else:
        form = UserLoginForm()
    return render(request, 'autentificare/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()

            UserProfile.objects.create(user=new_user, approved=False)

            # user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            # if user:
            #     auth_login(request, user)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')

            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'autentificare/register.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


@staff_member_required
def approve_users(request):
    users_to_approve = UserProfile.objects.filter(approved=False)

    context = {
        'users_to_approve': users_to_approve
    }
    return render(request, 'autentificare/approve_users.html', context)


@staff_member_required
def approve_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    user_profile.approved = True
    user_profile.save()
    # Poți adăuga aici și un mesaj de confirmare pentru admin

    return redirect('approve_users')

####carti


def imprumutaCarte(request, carte_id):
    carte = get_object_or_404(Carte, id=carte_id)
    if carte.disponibil:
        carte.disponibil = False
        carte.utilizator_imprumutat = request.user
        carte.setDataRevenire()
        carte.save()
        messages.success(request, 'Ati imprumutat cartea cu succes')
        print('Ati imprumutat cartea cu succes')

    return render(request, 'autentificare/home.html')


def raportCarte(request):
    carti_imprumutate = Carte.objects.filter(disponibil=False)
    carti_disponibile = Carte.objects.filter(disponibil=True)
    context = {'carti_imprumutate': carti_imprumutate,
               'carti_disponibile': carti_disponibile}

    return render(request, 'raport.html', context)