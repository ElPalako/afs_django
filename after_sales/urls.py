from django.urls import path
from django.contrib.auth import views as auth_views #Import wbudowanych widoków
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('create_ticket/', views.create_ticket_view, name='create_ticket'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ticket_list/', views.ticket_list_view, name='ticket_list'),
    path('ticket_detail/<int:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
    path('ticket_detail/<int:ticket_id>/update-status/', views.update_ticket_status, name='update_status'),
]