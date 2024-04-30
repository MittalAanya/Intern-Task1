from django.urls import path
from account import views
urlpatterns = [
    path('',views.SignupView,name='signup'),
    path('login/',views.LoginView,name='login'),
    path('home/',views.home,name='home'),
    path('logout/',views.LogoutView,name='logout'), 
    
]