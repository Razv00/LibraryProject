from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('imprumuta-carte/<int:carte_id>/',views.imprumutaCarte,name='imprumuta-carte'),
    path('raport',views.raportCarte,name = 'raport-carte'),
    path('approve-users/', views.approve_users, name='approve_users'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
]