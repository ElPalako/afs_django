from django.db import models
from django.contrib.auth.models import User
from after_sales.models import BusinessPartner

#Tabela rozszerzająca domyślnego Usera
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.ForeignKey(BusinessPartner, on_delete=models.SET_NULL, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"UserProfile: {self.user.username} - {self.company}"
