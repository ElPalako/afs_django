from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Orders
from users.models import UserProfile
from .forms import NewOrderForm
from django.db.models import Q
from .permissions import can_create_update_order

@login_required(login_url='login')
@user_passes_test(can_create_update_order, login_url='/')
def create_order_view(request):
    # Jeśli użytkownik kliknął "Zapisz" (wysłał dane formularza)
    if request.method == 'POST':
        form = NewOrderForm(request.POST)
        if form.is_valid(): # Django sam sprawdza, czy wpisano maile, daty itp.
            
            # 1. PAUZA: Tworzymy obiekt zgłoszenia z formularza, ale NIE zapisujemy go jeszcze w bazie
            order = form.save(commit=False)
            # 2. Przypisujemy Twórcę (zalogowany user)
            order.created_by = request.user
            # 3. Przypisujemy firmę (z modelu UserProfile, pole 'company')
            # (Używamy hasattr jako tarczy - w razie gdyby np. superuser nie miał profilu)
            if hasattr(request.user, 'profile'):
                order.business_partner = request.user.profile.company
                
            # 3. ZAPIS: Teraz kompletne zgłoszenie z przypisaną firmą leci na serwer!
            order.save()
            # MAGIA HTMX: Sprawdzamy, czy to zapytanie wysłane w tle
            if request.headers.get('HX-Request'):
                # Zwracamy czysty HTML z informacją o sukcesie. 
                # Opakowujemy to w tag <form>, żeby hx-select go poprawnie przechwycił!
                return HttpResponse("""
                    <form style="text-align: center; padding: 2rem;">
                        <h2 style="color: #10b981;">✅ Zamówienie zapisane pomyślnie!</h2>
                        <button type="button" onclick="location.reload()">Dodaj kolejne</button>
                    </form>
                """)
    # Jeśli użytkownik po prostu wszedł na stronę (GET)
    else:
        form = NewOrderForm()
    # Wysyłamy pusty formularz do szablonu HTML    
    return render(request, 'orders/new_order.html', {'form': form})

@login_required(login_url='login')
def orders_list_view(request):
    # 1. Pobieramy to, co użytkownik wpisał w pasku i w co kliknął
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '-created_at') # Domyślnie od najnowszych
    
    # Podstawowe zapytanie (wszystkie tickety)
    orders = Orders.objects.filter(business_partner=request.user.profile.company).select_related('business_partner')
    
    # 2. Filtrujemy po wyszukiwaniu
    if search_query:
        # icontains = szukaj ignorując wielkość liter (case-insensitive)
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(business_partner__name__icontains=search_query)
        )
    
    # 3. SORTOWANIE (Sprawdzamy, czy przesłany parametr jest bezpieczny)
    allowed_sorts = [
        'order_number', '-order_number', 
        'created_at', '-created_at', 
        'business_partner__name', '-business_partner__name'
    ]
    if sort_by in allowed_sorts:
        orders = orders.order_by(sort_by)
    else:
        orders = orders.order_by('-created_at')
        
    # Pakujemy wszystko do pudełka i wysyłamy do HTML
    context = {
        'orders': orders,
        'search_query': search_query,
        'current_sort': sort_by,
    }
    return render(request, 'orders/order_list.html', context)

@login_required(login_url='login')
@user_passes_test(can_create_update_order, login_url='/')
def order_detail_view(request, order_id):
    # Szukamy zgłoszenia, jeśli go nie ma - wyrzucamy błąd 404 (nie znaleziono)
    order = get_object_or_404(Orders, id=order_id)
    
    # Pobieramy również numery seryjne oraz trackingi - w przyszłości
    #tracking = ticket.ticketcomponent_set.all().select_related('component')
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/order_detail.html', context)

@login_required(login_url='login')
@user_passes_test(can_create_update_order, login_url='/')
def update_order_inline(request, order_id):
    # Upewniamy się, że zapytanie to HTMX
    if request.method == 'POST' and request.headers.get('HX-Request'):
        # Wyciągamy zamówienie, ale TYLKO z firmy zalogowanego użytkownika
        try:
            order = Orders.objects.get(id=order_id, business_partner=request.user.profile.company)
        except Orders.DoesNotExist:
            return HttpResponse("Brak dostępu", status=403)
        
        # Wymieniamy pola, na których edycję z poziomu tabeli pozwalamy
        allowed_fields = ['qty', 'material']
        
        # HTMX wysyła dane w formie słownika, np. {'qty': '5'} lub {'material': 'SHW/RMC/0001N'}
        # Przeszukujemy naszą białą listę i sprawdzamy, czy takie pole przyszło w POST
        for field in allowed_fields:
            if field in request.POST:
                new_value = request.POST.get(field)
                
                # setattr() podmienia dynamicznie pole
                setattr(order, field, new_value)
                order.save()
        
                # Zwracamy zaktualizowaną wartość wyciągniętą prosto z obiektu
                return HttpResponse(order.qty)
    
    return HttpResponse(status=400)