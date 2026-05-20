from django.contrib import admin
from .models import Shipment, Return

# Register your models here.

admin.site.register(Shipment)
admin.site.register(Return)