from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BaseLogistic(models.Model):
    business_partner = models.ForeignKey('after_sales.BusinessPartnerBranch', on_delete=models.RESTRICT) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    status = models.CharField(max_length=50)
    
    class Meta:
        abstract = True # <--- To sprawia, że tabela nie jest tworzona a służy jako wzró dla innych tabel (przejmują one wskazane we wzorze pola)

class Shipment(BaseLogistic):
    class ParcelType(models.TextChoices):
        PARCEL = 'PARCEL', 'Paczka'
        PALLET = 'PALLET', 'Paleta'
    class ParcelSize(models.TextChoices):
        SMALL = 'SMALL', 'Mała'
        MEDIUM = 'MEDIUM', 'Średnia'
        BIG = 'BIG', 'Duża'
    carrier = models.ForeignKey('after_sales.BusinessPartner', on_delete=models.RESTRICT)
    tracking = models.CharField(max_length=30)
    shipment_date = models.DateField()
    delivery_Date = models.DateField()
    comment = models.TextField()
    parcel_type = models.CharField(choices=ParcelType)
    size = models.CharField(choices=ParcelSize)
    dimensions = models.CharField(max_length=50, null=True)
    weight = models.CharField(max_length=10)
    carrier_document = models.CharField(max_length=50)
    customs_document = models.CharField(max_length=50)
    packing_list = models.CharField(max_length=50)
    fv_proforma = models.CharField(max_length=50)
    
    def __str__(self):
        return f"({self.id}, {self.business_partner.name},{self.carrier}, {self.tracking})"
    

class Return(BaseLogistic):
    reason = models.TextField()
    
    def __str__(self):
        return f"{self.id}, {self.business_partner.name}"
    