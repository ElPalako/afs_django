from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required #Importujemy kłódkę
from .models import ServiceTicket, Stock
from .forms import ServiceTicketForm
from django.db.models import Q

@login_required(login_url='login')
def dashboard_view(request):
    user_profile = getattr(request.user, 'profile', None)

    # 1. Zliczamy wszystkie zgłoszenia
    total_tickets = ServiceTicket.objects.count()
    
    # 2. Zliczamy zgłoszenia po TWOICH statusach
    tickets_open = ServiceTicket.objects.filter(status='OPEN').count()
    tickets_in_progress = ServiceTicket.objects.filter(status='IN_PROGRESS').count()
    tickets_waiting = ServiceTicket.objects.filter(status='WAITING_FOR_COMPONENTS').count()
    tickets_ready = ServiceTicket.objects.filter(status='READY_FOR_PICKUP').count()
    
    # 3. Alerty Magazynowe
    low_stock = Stock.objects.filter(quantity__lt=5).select_related('component')[:5]

    context = {
        'profile': user_profile,
        'total_tickets': total_tickets,
        'tickets_open': tickets_open,
        'tickets_in_progress': tickets_in_progress,
        'tickets_waiting': tickets_waiting,
        'tickets_ready': tickets_ready,
        'low_stock': low_stock,
    }
    
    return render(request, 'after_sales/dashboard.html', context)


@login_required(login_url='login') #Ta dekoracja sprawia, że tylko zalogowani użytkownicy mogą zobaczyć ten widok. Jeśli nie są zalogowani, zostaną przekierowani do strony logowania.
def create_ticket_view(request):
    # Jeśli użytkownik kliknął "Zapisz" (wysłał dane formularza)
    if request.method == 'POST':
        form = ServiceTicketForm(request.POST)
        if form.is_valid(): # Django sam sprawdza, czy wpisano maile, daty itp.
            form.save()     # Zapisujemy do bazy!
            # MAGIA HTMX: Sprawdzamy, czy to zapytanie wysłane w tle
            if request.headers.get('HX-Request'):
                # Zwracamy czysty HTML z informacją o sukcesie. 
                # Opakowujemy to w tag <form>, żeby hx-select go poprawnie przechwycił!
                return HttpResponse("""
                    <form style="text-align: center; padding: 2rem;">
                        <h2 style="color: #10b981;">✅ Zgłoszenie zapisane pomyślnie!</h2>
                        <button type="button" onclick="location.reload()">Dodaj kolejne</button>
                    </form>
                """)
    # Jeśli użytkownik po prostu wszedł na stronę (GET)
    else:
        form = ServiceTicketForm()
    # Wysyłamy pusty formularz do szablonu HTML    
    return render(request, 'after_sales/create_ticket.html', {'form': form})

@login_required(login_url='login')
def ticket_list_view(request):
    # 1. Pobieramy to, co użytkownik wpisał w pasku i w co kliknął
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '-created_at') # Domyślnie od najnowszych
    
    # Podstawowe zapytanie (wszystkie tickety)
    tickets = ServiceTicket.objects.all().select_related('customer', 'device_model')
    
    # 2. Filtrujemy po wyszukiwaniu
    if search_query:
        # icontains = szukaj ignorując wielkość liter (case-insensitive)
        tickets = tickets.filter(
            Q(ticket_number__icontains=search_query) |
            Q(customer__name__icontains=search_query) |
            Q(device_model__name__icontains=search_query)
        )
    
    # 3. SORTOWANIE (Sprawdzamy, czy przesłany parametr jest bezpieczny)
    allowed_sorts = [
        'ticket_number', '-ticket_number', 
        'created_at', '-created_at', 
        'customer__name', '-customer__name'
    ]
    if sort_by in allowed_sorts:
        tickets = tickets.order_by(sort_by)
    else:
        tickets = tickets.order_by('-created_at')
        
    # Pakujemy wszystko do pudełka i wysyłamy do HTML
    context = {
        'tickets': tickets,
        'search_query': search_query,
        'current_sort': sort_by,
    }
    return render(request, 'after_sales/ticket_list.html', context)