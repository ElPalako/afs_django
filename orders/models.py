from django.db import models
from django.contrib.auth.models import User
from after_sales.models import BusinessPartner, ServiceTicket, Component

#Tabela trackingów - komponenty
class OrdersTracking(models.Model):
    class ParcelType(models.TextChoices):
        PACKAGE = 'PACKAGE', 'Paczka'
        PALLET = 'PALLET', 'Paleta'
    tracking = models.CharField(max_length=100)
    carrier = models.CharField(max_length=50)
    shipment_date = models.DateField()
    delivery_date = models.DateField()
    comment = models.TextField()
    status = models.CharField(max_length=100)
    parcel_type = models.CharField(choices=ParcelType)
    size = models.CharField()
    dimensions = models.CharField()
    weight = models.CharField()
    carrier_documents = models.CharField()
    customs_documents = models.CharField()
    packing_list = models.CharField()
    fv_proforma = models.CharField()
    recipient_id = models.ForeignKey(
        BusinessPartner,
        on_delete = models.RESTRICT,
    )

#Tabela zamówień na części
class Orders(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = 'NEW', 'Nowe'
        IN_PROGRESS = 'IN_PROGRESS', 'W realizacji'
        WAITING_FOR_COMPONENTS = 'WAITING_FOR_COMPONENTS', 'Czekające na części'
        DISSASEMBLY = "DISSASEMBLY", "Oczekuje na demontaż"
        PR = 'PR', "Oczekuje na Panel Repair"
        READY_FOR_PICKUP = 'READY_FOR_PICKUP', 'Gotowe do odbioru'
        SHIPPED = 'SHIPPED', 'Wysłane'
        DELIVERED = 'DELIVERED', 'Dostarczone'
        NOT_REPAIRABLE = 'NOT_REPAIRABLE', 'Nie do naprawy'
        NOT_PROFITABLE = 'NOT_PROFITABLE', 'Naprawa nieopłacalna'
        CLOSED = 'CLOSED', 'Zamknięte'
    class Purpose(models.TextChoices):
        IW = 'IN_WARRANTY', 'Gwarancja'
        OOW = 'OUT_OF_WARRANTY', 'Poza gwarancją'
        BUFFER = 'BUFFER', 'Buffer'
    status = models.CharField(choices=OrderStatus, default=OrderStatus.NEW)
    order_number = models.CharField(max_length=50, blank=True, null=True)
    purpose = models.CharField(choices=Purpose, default='IN_WARRANTY')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    ticket = models.ForeignKey(
        ServiceTicket,
        on_delete=models.RESTRICT,
        null=True
    )
    business_partner = models.ForeignKey(
        BusinessPartner,
        on_delete=models.RESTRICT,       
    )
    material = models.CharField(max_length=50, null=True)
    qty = models.IntegerField()
    description = models.CharField(max_length=255)
    qty_to_be_realized = models.IntegerField(default=0)
    internal_order_number = models.CharField(null=True)
    material_prepared = models.CharField(max_length=50, null=True)
    qty_prepared = models.IntegerField(default=0)
    tracking = models.ForeignKey(
        OrdersTracking,
        on_delete=models.RESTRICT,
        null=True,
    )
    comment = models.TextField(null=True)
    comment_for_tpm = models.TextField(null=True)
    fulfillment_start_date = models.DateField(null=True)
    fulfillment_comment = models.CharField(max_length=255)
    fulfillment_finish_date = models.DateField(null=True)
    material_price_pln = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    material_price_eur = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    article_number = models.CharField(max_length=50)
    original_article_number = models.CharField(max_length=50)
    
    
    @property
    def client_status(self):
        # Słownik (mapa), który tłumaczy nasze statusy na statusy dla klienta
        status_map = {
            self.OrderStatus.NEW: 'Nowe',
            # Kilka różnych statusów wewnętrznych daje ten sam komunikat dla klienta
            self.OrderStatus.WAITING_FOR_COMPONENTS: 'W realizacji',
            self.OrderStatus.DISASSEMBLY: 'W realizacji',
            self.OrderStatus.IN_PROGRESS: 'W realizacji',
            self.OrderStatus.PR: 'W realizacji',
            self.OrderStatus.IN_PROGRESS: 'W realizacji',
            self.OrderStatus.READY_FOR_PICKUP: 'Gotowe do odbioru',
            self.OrderStatus.SHIPPED: 'Wysłane',
            self.OrderStatus.DELIVERED: 'Dostarczone',
            self.OrderStatus.NOT_REPAIRABLE: 'Nie do naprawy',
            self.OrderStatus.NOT_PROFITABLE: 'Naprawa nieopłacalna',
            self.OrderStatus.CLOSED: 'Zamknięte',
        }
        
        # Pobieramy przetłumaczony status. 
        # Jeśli jakiegoś zapomnisz dodać do słownika, domyślnie zwróci 'Przetwarzane'
        return status_map.get(self.status, 'Przetwarzane')
    
    def __str__(self):
        return f"Order: {self.order_number} - {self.get_status_display()}"
    
    #Tabela numerów seryjnych - komponenty
class OrdersSerialNumber(models.Model):
    serial_number = models.CharField(max_length=100)
    serial_number_scep = models.CharField(max_length=100)
    order = models.ForeignKey(
        Orders,
        on_delete=models.RESTRICT,
    )