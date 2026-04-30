from django.urls import path
from django.contrib.auth import views as auth_views #Import wbudowanych widoków
from . import views

urlpatterns = [
    path('zamówienia/', views.orders_list_view, name='orders-list'),
    path('nowe-zamówienie/', views.create_order_view, name='create-order'),
    path('zamówienie/<int:order_id>/', views.order_detail_view, name='order-detail'),
    # "Niewidzialny" endpoint do edycji w locie
    path('zamówienie/<int:order_id>/update-inline/', views.update_order_inline, name='update_order_inline'),
]