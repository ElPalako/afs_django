from django.contrib import admin
from .models import Customer, BusinessPartner, ServiceTicket, TicketComponent

# Rejestrujemy wszystkie nasze modele, żeby były widoczne w panelu admina
admin.site.register(Customer)
admin.site.register(BusinessPartner)
admin.site.register(TicketComponent)

@admin.register(ServiceTicket)
class ServiceTicketAdmin(admin.ModelAdmin):
    _my_fields = ('id','ticket_number', 'customer', 'device_model', 'is_warranty', 'purchase_date', 'status', 'created_at', 'business_partner', 'description')
    list_display = _my_fields
    list_filter = _my_fields
    search_fields = _my_fields