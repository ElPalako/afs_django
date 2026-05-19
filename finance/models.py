from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
# Marże
class Margin(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT ,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
        
    def __str__(self):
        return f"{self.name}"

# Detale marż
class MarginDetail(models.Model):
    margin = models.ForeignKey(Margin, on_delete=models.RESTRICT, related_name='details')
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT ,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price_from = models.DecimalField(max_digits=10, decimal_places=2)
    price_to = models.DecimalField(max_digits=10, decimal_places=2)
    margin_value = models.DecimalField(max_digits=10, decimal_places=2)
    priority = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}: od {self.price_from} do {self.price_to}"