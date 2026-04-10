from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Tabela klientów
class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
#Tabela partnerów binzesowych
class BusinessPartner(models.Model):
    class PartnerType(models.TextChoices):
        MANUFACTURER = 'MANUFACTURER', 'Producent'
        DISTRIBUTOR = 'DISTRIBUTOR', 'Dystrybutor'
        SERVICE_CENTER = 'SERVICE_CENTER', 'Serwis Zewnętrzny'
        B2B_CLIENT = 'B2B_CLIENT', 'Klient Firmowy'

    name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=50, blank=True, null=True) # NIP / VAT No
    partner_type = models.CharField(max_length=20, choices=PartnerType.choices, default=PartnerType.SERVICE_CENTER)
    
    def __str__(self):
        return f"BusinessPartner: {self.name} ({self.get_partner_type_display()})"

#Tabela rozszerzająca domyślnego Usera
class UserProfile(models.Model):
    #Słownik ról użytkowników
    class UserRole(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        ORDER_CREATE = 'ORDER_CREATE', 'Tworzenie Zamówień'
        ORDER_FULFILLMENT = 'ORDER_FULFILLMENT', 'Realizacja Zamówień'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=100, choices=UserRole.choices, default="")
    company = models.ForeignKey(BusinessPartner, on_delete=models.SET_NULL, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"UserProfile: {self.user.username}"

#Tabela modeli urządzeń
class DeviceModel(models.Model):
    name = models.CharField(max_length=150)
    manufacturer = models.ForeignKey(
        BusinessPartner, 
        on_delete=models.RESTRICT, 
        limit_choices_to={'partner_type': 'MANUFACTURER'})

    def __str__(self):
        return f"DeviceModel: {self.name} {self.manufacturer.name}"

#Tabela zgłoszeń serwisowych
class ServiceTicket(models.Model):
    ticket_number = models.CharField(max_length=50, unique=True)
    serial_number = models.CharField(max_length=100)
    is_warranty = models.BooleanField(default=True)
    purchase_date = models.DateField(blank=True, null=True)
    repair_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE)
    device_model = models.ForeignKey(
        DeviceModel, 
        on_delete=models.RESTRICT)
    
    def __str__(self):
        return f"Ticket: {self.ticket_number} - {self.serial_number}"
    
#Tabela komponentów
class Component(models.Model):
    part_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    moq = models.PositiveIntegerField(default=1) # Minimum Order Quantity
    manufacturer = models.ForeignKey(
        BusinessPartner,
        on_delete = models.RESTRICT,
        limit_choices_to = {'partner_type': 'MANUFACTURER'},
        blank = True,
        null = True
        )
    
    def __str__(self):
        return f"Component: {self.part_number} for {self.name}"

#Tabela ze stockiem magazynowym
class Stock(models.Model):
    component = models.ForeignKey(
        Component, 
        on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField(default=0)
    storage_location = models.CharField(max_length=10, blank=True, null=True) # Lokalizacja w magazynie
    plant = models.CharField(max_length=10, blank=True, null=True) # Lokalizacja w magazynie

    def __str__(self):
        return f"Stock: {self.component.part_number} - {self.quantity} pcs at {self.storage_location}"

#Komponenty użyte w naprawie
class TicketComponent(models.Model):
    ticket_number = models.ForeignKey(
        ServiceTicket, 
        on_delete=models.CASCADE)
    component = models.ForeignKey(
        Component, 
        on_delete=models.RESTRICT)
    quantity_used = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"TicketComponent: {self.component.part_number}, {self.quantity_used} used in {self.ticket_number.ticket_number}"