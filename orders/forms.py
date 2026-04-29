from django import forms
from .models import Orders

class NewOrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        # Wybieramy, które pola z bazy chcemy pokazać pracownikowi
        fields = ['order_number', 'ticket', 'material', 'qty', 'description', 'purpose']
        widgets = {
            'order_number': forms.TextInput(attrs={'class': 'input-standard', 'placeholder': 'Wpisz numer zamówienia...'}),
            'ticket': forms.Select(attrs={'class': 'input-standard'}),
            'material': forms.TextInput(attrs={'class': 'input-standard'}),
            'qty': forms.NumberInput(attrs={'class': 'input-standard', 'placeholder': 'Wpisz ilość...'}),
            'description': forms.Textarea(attrs={'class': 'textarea-standard', 'placeholder': 'Wprowadź opis...', 'rows': 4}),
            'purpose': forms.Select(attrs={'class': 'input-standard'}),
        }