from django.shortcuts import render, redirect
from .forms import ServiceTicketForm

def create_ticket_view(request):
    # Jeśli użytkownik kliknął "Zapisz" (wysłał dane formularza)
    if request.method == 'POST':
        form = ServiceTicketForm(request.POST)
        if form.is_valid(): # Django sam sprawdza, czy wpisano maile, daty itp.
            form.save()     # Zapisujemy do bazy!
            return redirect('/admin/after_sales/serviceticket/') # Na razie odsyłamy go do panelu admina
    # Jeśli użytkownik po prostu wszedł na stronę (GET)
    else:
        form = ServiceTicketForm()
    # Wysyłamy pusty formularz do szablonu HTML    
    return render(request, 'after_sales/create_ticket.html', {'form': form})

