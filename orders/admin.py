from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportMixin
from .models import Orders, OrdersSerialNumber

# Rejestrujemy wszystkie nasze modele, żeby były widoczne w panelu admina
# przykład: admin.site.register(OrdersSerialNumber)

# Rejestracja zaawansowana - widok tabeli@admin.register(Stock)
@admin.register(Orders)
class OrdersAdmin(ImportExportMixin, SimpleHistoryAdmin): # Kolejność ma znaczenie
    # Kolumny, które chcemy widzieć w tabeli
    list_display = ('order_number', 'material', 'qty', 'status', 'business_partner', 'purpose', 'ticket', 'material', 'description', 'internal_order_number')
    # Filtry po prawej stronie ekranu
    list_filter = ('order_number', 'material', 'status', 'business_partner', 'purpose', 'ticket', 'material', 'description', 'internal_order_number')
    # Pasek wyszukiwania!
    search_fields = ('order_number', 'material', 'status', 'business_partner__name', 'ticket__ticket_number', 'material', 'description', 'internal_order_number')
    
@admin.register(OrdersSerialNumber)
class OrdersSerialNumberAdmin(ImportExportMixin, SimpleHistoryAdmin):
    list_display = ('serial_number', 'serial_number_scep', 'order')
    list_filter = ('serial_number', 'serial_number_scep')
    search_fields = ('serial_number', 'serial_number_scep')