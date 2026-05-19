from django.db import models

# Create your models here.

class Margin(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT ,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    margin_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    price_from = models.DecimalField()
    price_to = models.DecimalField()
    margin_value = models.DecimalField()
    priority = models.PositiveIntegerField()
        
    def __str__(self):
        return f"{self.name}"