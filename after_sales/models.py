from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Klienci (użytkownicy końcowi)
class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return (self.name)
    
# Firmy, partnerzy biznesowi
class BusinessPartner(models.Model):
    class PartnerType(models.TextChoices):
        SCEP = 'SCEP', 'SCEP'
        MANUFACTURER = 'MANUFACTURER', 'Producent'
        DISTRIBUTOR = 'DISTRIBUTOR', 'Dystrybutor'
        SERVICE_CENTER = 'SERVICE_CENTER', 'Serwis Zewnętrzny'
        B2B_CLIENT = 'B2B_CLIENT', 'Klient Firmowy'
        CARRIER = 'CARRIER', 'Przewoźnik'

    created_by = models.ForeignKey(User, on_delete=models.RESTRICT ,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    name = models.CharField(max_length=255)
    partner_type = models.CharField(max_length=20, choices=PartnerType.choices, default=PartnerType.SERVICE_CENTER)
    administrator = models.ForeignKey('users.UserProfile', on_delete=models.RESTRICT, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    company_number = models.CharField(max_length=50, null=True, blank=True)
    vendor_number = models.CharField(max_length=50, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    call_center_email = models.EmailField(null=True, blank=True)
    call_center_phone = models.CharField(max_length=50, null=True, blank=True)
    accounting_email = models.EmailField(null=True, blank=True)
    accounting_phone = models.CharField(max_length=50, null=True, blank=True)
    street_name = models.CharField(max_length=255, null=True, blank=True)
    street_number = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    delivery_terms = models.CharField(max_length=50, null=True, blank=True)
    fv_proforma = models.BooleanField(default=True)
    margin = models.ForeignKey("finance.Margin", on_delete=models.RESTRICT, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_partner_type_display()})"

# Branche firm
class BusinessPartnerBranch(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT ,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    is_main_branch = models.BooleanField(default=False)
    business_partner_id = models.ForeignKey(BusinessPartner, on_delete=models.RESTRICT, null=True)
    is_active = models.BooleanField(default=True)
    contact_email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    parts_email = models.EmailField(null=True, blank=True)
    parts_phone = models.CharField(max_length=50, null=True, blank=True)
    service_email = models.EmailField(null=True, blank=True)
    service_phone = models.CharField(max_length=50, null=True, blank=True)
    street_name = models.CharField(max_length=255, null=True, blank=True)
    street_number = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
        
    def __str__(self):
        return f"{self.name}, {self.business_partner_id.name}"

#Tabela zgłoszeń serwisowych
class ServiceTicket(models.Model):
    class TicketStatus(models.TextChoices):
        OPEN = 'OPEN', 'Otwarte'
        IN_PROGRESS = 'IN_PROGRESS', 'W realizacji'
        WAITING_FOR_COMPONENTS = 'WAITING_FOR_COMPONENTS', 'Czekające na części'
        DISASSEMBLY = "DISASSEMBLY", "Oczekuja na demontaż"
        READY_FOR_PICKUP = 'READY_FOR_PICKUP', 'Gotowe do odbioru'
        SHIPPED = 'SHIPPED', 'Wysłane'
        DELIVERED = 'DELIVERED', 'Dostarczone'
        NOT_REPAIRABLE = 'NOT_REPAIRABLE', 'Nie do naprawy'
        CLOSED = 'CLOSED', 'Zamknięte'
    ticket_number = models.CharField(max_length=50, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    serial_number = models.CharField(max_length=100, db_index=True)
    is_warranty = models.BooleanField(default=True)
    purchase_date = models.DateField(blank=True, null=True)
    repair_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    device_model = models.ForeignKey('inventory.DeviceModel', on_delete=models.RESTRICT)
    status = models.CharField(max_length=100, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    business_partner = models.ForeignKey(
        BusinessPartner,
        on_delete=models.RESTRICT,
        null=True,        
    )
    description = models.TextField(blank=True, null=True)
    
    @property
    def client_status(self):
        # Słownik (mapa), który tłumaczy nasze statusy na statusy dla klienta
        status_map = {
            self.TicketStatus.OPEN: 'Przyjęto do serwisu',
            # Kilka różnych statusów wewnętrznych daje ten sam komunikat dla klienta
            self.TicketStatus.WAITING_FOR_COMPONENTS: 'W realizacji',
            self.TicketStatus.DISASSEMBLY: 'W realizacji',
        }
        
        # Pobieramy przetłumaczony status. 
        # Jeśli jakiegoś zapomnisz dodać do słownika, domyślnie zwróci 'Przetwarzane'
        return status_map.get(self.status, 'Przetwarzane')
    
    def __str__(self):
        return self.ticket_number
    
#Komponenty użyte w naprawie
class TicketComponent(models.Model):
    ticket_number = models.ForeignKey(
        ServiceTicket, 
        on_delete=models.RESTRICT)
    component = models.ForeignKey(
        'inventory.Component', 
        on_delete=models.RESTRICT)
    quantity_used = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.component.part_number}, {self.quantity_used} used in {self.ticket_number.ticket_number}"