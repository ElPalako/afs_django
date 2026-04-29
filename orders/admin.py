from django.contrib import admin
from .models import Orders, OrdersTracking, OrdersSerialNumber

# Rejestrujemy wszystkie nasze modele, żeby były widoczne w panelu admina
admin.site.register(OrdersTracking)
admin.site.register(OrdersSerialNumber)

# Rejestracja zaawansowana - widok tabeli@admin.register(Stock)
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    # Pomocnicza zmienna (zwykle z podłogą na początku, żeby pokazać, że jest "prywatna")
    _my_fields = ('order_number', 'qty', 'material')
    # Kolumny, które chcemy widzieć w tabeli
    list_display = _my_fields
    # Filtry po prawej stronie ekranu
    list_filter = _my_fields
    # Pasek wyszukiwania!
    search_fields = _my_fields