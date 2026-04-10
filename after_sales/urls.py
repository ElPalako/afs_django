from django.urls import path
from . import views

urlpatterns = [
    path('nowe-zgloszenie/', views.create_ticket_view, name='create-ticket'),
]