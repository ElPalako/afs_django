from django.db import models
from django.contrib.auth.models import User
from after_sales.models import BusinessPartner

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
        return f"UserProfile: {self.user.username} - {self.get_role_display()}"
