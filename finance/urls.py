from django.urls import path
from . import views
from after_sales import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
]