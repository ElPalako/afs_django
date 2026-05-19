from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Tabela klientów
class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return (self.name)
    
#Tabela partnerów binzesowych
class BusinessPartner(models.Model):
    class PartnerType(models.TextChoices):
        SCEP = 'SCEP', 'SCEP'
        MANUFACTURER = 'MANUFACTURER', 'Producent'
        DISTRIBUTOR = 'DISTRIBUTOR', 'Dystrybutor'
        SERVICE_CENTER = 'SERVICE_CENTER', 'Serwis Zewnętrzny'
        B2B_CLIENT = 'B2B_CLIENT', 'Klient Firmowy'

    name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=50, blank=True, null=True) # NIP / VAT No
    partner_type = models.CharField(max_length=20, choices=PartnerType.choices, default=PartnerType.SERVICE_CENTER)
    
    def __str__(self):
        return f"{self.name} ({self.get_partner_type_display()})"

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