from django.contrib import admin
from .models import Stock, DeviceModel, Component, ComponentCategory
# Register your models here.

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    _my_fields = ('id','component', 'quantity', 'storage_location', 'plant', 'vendor')
    # Kolumny, które chcemy widzieć w tabeli
    list_display = _my_fields
    # Filtry po prawej stronie ekranu
    list_filter = _my_fields
    # Pasek wyszukiwania!
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