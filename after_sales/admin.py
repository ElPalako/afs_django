from django.contrib import admin
from .models import Customer, BusinessPartner, DeviceModel, ServiceTicket, Component, Stock, TicketComponent, ComponentCategory

# Rejestrujemy wszystkie nasze modele, żeby były widoczne w panelu admina
admin.site.register(Customer)
admin.site.register(BusinessPartner)
admin.site.register(TicketComponent)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    _my_fields = ('id','component', 'quantity', 'storage_location', 'plant', 'vendor')
    # Kolumny, które chcemy widzieć w tabeli
    list_display = _my_fields
    # Filtry po prawej stronie ekranu
    list_filter = _my_fields
    # Pasek wyszukiwania!
    search_fields = _my_fields

@admin.register(ServiceTicket)
class ServiceTicketAdmin(admin.ModelAdmin):
    _my_fields = ('id','ticket_number', 'customer', 'device_model', 'is_warranty', 'purchase_date', 'status', 'created_at', 'business_partner', 'description')
    list_display = _my_fields
    list_filter = _my_fields
    search_fields = _my_fields
    
@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    _my_fields = ('id','fg_code','model_name', 'manufacturer', 'device_category')
    list_display = _my_fields
    list_filter = _my_fields
    search_fields = _my_fields

@admin.register(Component)    
class ComponentAdmin(admin.ModelAdmin):
    _my_fields = ('id','part_number', 'description', 'price', "moq", 'manufacturer', 'category')
    list_display = _my_fields
    list_filter = _my_fields
    search_fields = _my_fields
    
@admin.register(ComponentCategory)    
class ComponentCategoryAdmin(admin.ModelAdmin):
    _my_fields = ('id','category_name', 'description', 'sn_need')
    list_display = _my_fields
    list_filter = _my_fields
    search_fields = _my_fields