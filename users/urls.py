from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Korzystamy z wbudowanego widoku Django, podmieniamy tylko HTML-a
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name = 'register')
]