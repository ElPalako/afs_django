from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Tabela modeli urządzeń
class DeviceModel(models.Model):
    
    class DeviceCategory(models.TextChoices):
        TV = 'TV', 'Telewizor'
        AUD = 'Audio', 'Audio'
        SAS = 'SAS', 'SAS/SDA'
        EBIKE = 'Ebike', 'Rower elektryczny' 
        ESC = 'Escooter', 'Hulajnoga elektryczna'
    
    fg_code = models.CharField(max_length=50, db_index=True, unique=True)
    model_name = models.CharField(max_length=150)
    manufacturer = models.ForeignKey(
        'after_sales.BusinessPartner', 
        on_delete=models.RESTRICT, 
        limit_choices_to={'partner_type': 'MANUFACTURER'})
    device_category = models.CharField(max_length=200, choices=DeviceCategory.choices, null=True) 

    def __str__(self):
        return f"{self.fg_code}"
    
# Tabela kategorii komponentów
    
class ComponentCategory(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    sn_need = models.BooleanField(default=False)
    
    def __str__(self):
        return self.category_name
    
# Tabela komponentów

class Component(models.Model):
    part_number = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    moq = models.PositiveIntegerField(default=1) # Minimum Order Quantity
    manufacturer = models.ForeignKey(
        'after_sales.BusinessPartner',
        on_delete = models.RESTRICT,
        limit_choices_to = {'partner_type': 'MANUFACTURER'},
        blank = True,
        null = True
        )
    category = models.ForeignKey(
        ComponentCategory,
        on_delete=models.RESTRICT,
        null=True)
    
    def __str__(self):
        return f"{self.part_number} - {self.description}"

#Tabela ze stockiem magazynowym
class Stock(models.Model):
    component = models.ForeignKey(
        Component, 
        on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField(default=0)
    storage_location = models.CharField(max_length=10, blank=True, null=True)
    plant = models.CharField(max_length=10, blank=True, null=True)
    vendor = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.component.part_number} - {self.quantity} pcs at {self.storage_location}"