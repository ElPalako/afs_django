from django.db import transaction
from django.core.exceptions import ValidationError
from .models import ServiceTicket, Component, Stock, TicketComponent

def add_part_to_ticket(ticket_id: int, component_id: int, quantity_used: int):
    """
    Dodaje komponent do zgłoszenia i automatycznie zdejmuje go z magazynu.
    """
    # Zabezpieczenie przed ujemnymi wartościami
    if quantity_used <= 0:
        raise ValidationError("Ilość zużytych części musi być większa niż zero.")
    
    #Rozpoczęcie transakcji bazy danych (alob przjdzie cała transakca lub żadna)
    with transaction.atomic():
       # 1. Odnajdujemy zgłoszenie i komponent w bazie
       ticket = ServiceTicket.objects.get(id=ticket_id)
       component = Component.objects.get(id=component_id)
       
       # 2. Szukamy na magazynie miejsca, gdzie leży ten komponent i ma wystarczającą ilość.
       # Używamy .first() by wziąć pierwszą półkę z brzegu, która spełnia warunek.
       stock = Stock.objects.filter(component=component, quantity__gte=quantity_used).first()
       
       if not stock:
           #Jeśli nie znaleźliśmy wystarczającej ilości komponentu, rzucamy wyjątek i przerywamy akcję
           raise ValidationError(f"Nie ma wystarczającej ilości komponentu {component.part_number} w magazynie.")
       
       # 3. Odejmujemy ilość z magazynu
       stock.quantity -= quantity_used
       stock.save()
       
       # 4. Dodajemy komponent do zgłoszenia
       # get_or_create to sprytna funkcja: jeśli mechanik już wcześniej dodał np. 1 filtr, 
       # a teraz dodaje kolejny, system nie stworzy drugiego rekordu, tylko zaktualizuje stary!
       ticket_part, created = TicketComponent.objects.get_or_create(
              ticket_number=ticket,
              component=component,
              defaults={'quantity_used': quantity_used}
         )
       
       # Dodajemy użyte sztuki i zapisujemy
       ticket_part.quantity_used += quantity_used
       ticket_part.save()
       
       return ticket_part