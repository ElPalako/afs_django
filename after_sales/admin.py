from django.contrib import admin
from .models import Customer, BusinessPartner, DeviceModel, ServiceTicket, Component, Stock, TicketComponent, UserProfile

# Rejestrujemy wszystkie nasze modele, żeby były widoczne w panelu admina
admin.site.register(Customer)
admin.site.register(BusinessPartner)
admin.site.register(DeviceModel)
admin.site.register(Component)
admin.site.register(TicketComponent)
admin.site.register(UserProfile)

# Rejestracja zaawansowana - widok tabeli@admin.register(Stock)
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    # Kolumny, które chcemy widzieć w tabeli
    list_display = ('component', 'quantity', 'storage_location')
    # Filtry po prawej stronie ekranu
    list_filter = ('storage_location', 'component__manufacturer')
    # Pasek wyszukiwania!
    search_fields = ('component__name', 'component__part_number')

@admin.register(ServiceTicket)
class ServiceTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'customer', 'device_model', 'is_warranty', 'purchase_date')
    list_filter = ('is_warranty', 'device_model')
    search_fields = ('ticket_number', 'serial_number', 'customer__name')