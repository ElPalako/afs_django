from django.urls import path
from django.contrib.auth import views as auth_views #Import wbudowanych widoków
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('nowe-zgloszenie/', views.create_ticket_view, name='create-ticket'),
    path('login/', auth_views.LoginView.as_view(template_name='after_sales/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]