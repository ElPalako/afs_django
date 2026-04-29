from django.contrib import admin
from .models import Orders, OrdersTracking, OrdersSerialNumber

# Rejestrujemy wszystkie nasze modele, żeby były widoczne w panelu admina
admin.site.register(OrdersTracking)
admin.site.register(OrdersSerialNumber)

# Rejestracja zaawansowana - widok tabeli@admin.register(Stock)
@admin.register(Orders)
class StockAdmin(admin.ModelAdmin):
    # Kolumny, które chcemy widzieć w tabeli
    list_display = ('order_number', 'qty', 'material')
    # Filtry po prawej stronie ekranu
    list_filter = ('order_number', 'qty', 'material')
    # Pasek wyszukiwania!
    search_fields = ('order_number', 'qty', 'material')