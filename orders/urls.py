from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.orders_list_view, name='orders_list'),
    path('create_order/', views.create_order_view, name='create_order'),
    path('order_detail/<int:order_id>/', views.order_detail_view, name='order_detail'),
    # "Niewidzialny" endpoint do edycji w locie
    path('order_update/<int:order_id>/update-inline/', views.update_order_inline, name='update_order_inline'),
]