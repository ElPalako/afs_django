from django import forms
from .models import ServiceTicket

class ServiceTicketForm(forms.ModelForm):
    class Meta:
        model = ServiceTicket
        # Wybieramy, które pola z bazy chcemy pokazać pracownikowi
        fields = ['ticket_number', 'customer', 'purchase_date', 'serial_number', 'is_warranty', 'device_model']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'customer': forms.Select(attrs={'class': 'input-standard'}),
            'device_model': forms.Select(attrs={'class': 'input-standard'}),
            'serial_number': forms.TextInput(attrs={'class': 'input-standard', 'placeholder': 'Wpisz numer SN...'}),
        }