from django.shortcuts import render, HttpResponse, get_object_or_404
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

@login_required(login_url='login')
def ticket_detail_view(request, ticket_id):
    # Szukamy zgłoszenia, jeśli go nie ma - wyrzucamy błąd 404 (nie znaleziono)
    ticket = get_object_or_404(ServiceTicket, id=ticket_id)
    
    # Pobieramy również listę części przypisanych do tego zgłoszenia
    parts_used = ticket.ticketcomponent_set.all().select_related('component')
    
    context = {
        'ticket': ticket,
        'parts_used': parts_used,
        # W przyszłości prześlemy tu też formularz dodawania częsci
    }
    
    return render(request, 'after_sales/ticket_detail.html', context)

@login_required(login_url='login')
def update_ticket_status(request, ticket_id):
    if request.method == 'POST':
        ticket = get_object_or_404(ServiceTicket, id=ticket_id)
        # Pobieramy nową wartość statusu przesłaną przez HTMX
        new_staus = request.POST.get('status')
        
        # Aktualizujemy model
        ticket.status = new_staus
        ticket.save()
        
        # Zwracamy TYLKO fragment HTML z nowym statusem
        # Używamy get_status_display() żęby pokazać ładną nazwę
        return HttpResponse(f"""
            <span class="px-3 py-1 text-sm font-bold rounded-full bg-blue-100 text-blue-800 transition-all duration-500">
                {ticket.get_status_display()}
            </span>
            <div class="text-xs text-green-600 mt-1 animate-bounce">Status zaktualizowany!</div>
        """)