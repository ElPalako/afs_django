from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required #Importujemy kłódkę
from .models import ServiceTicket, Stock
from .forms import ServiceTicketForm

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
    # Pobieramy wszystkie tickety. Znak minus '-' przed created_at oznacza "Malejąco" (od najnowszych)
    # .select_related() optymalizuje zapytania do bazy, żeby pobrać od razu dane klienta i urządzenia
    tickets = ServiceTicket.objects.all().order_by('-created_at').select_related('customer', 'device_model')
    
    return render(request, 'after_sales/ticket_list.html', {'tickets': tickets})