from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required #Importujemy kłódkę
from .models import ServiceTicket, Stock
from .forms import ServiceTicketForm

@login_required(login_url='login') #Ta dekoracja sprawia, że tylko zalogowani użytkownicy mogą zobaczyć ten widok. Jeśli nie są zalogowani, zostaną przekierowani do strony logowania.
def dashboard_view(request):
    # Pobieramy profil użytkownika (jeśli istnieje)
    user_profile = getattr(request.user, 'profile', None)
    
    # Statystyki RMA
    total_tickets = ServiceTicket.objects.count()
    warranty_tickets = ServiceTicket.objects.filter(is_warranty=True).count()
    paid_tickets = total_tickets - warranty_tickets
    
    # Alerty magazynowe (Szukamy części, których jest mniej niż 10 sztuk)
    low_stock_alerts = Stock.objects.filter(quantity__lt=10).select_related('component')[:10]
    
    # Pakujemy wszystko w jedną "paczkę" (słownik) i wysyłamy do szablonu
    context = {
        'profile': user_profile,
        'total_tickets': total_tickets,
        'warranty_tickets': warranty_tickets,
        'paid_tickets': paid_tickets,
        'low_stock_alerts': low_stock_alerts
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

