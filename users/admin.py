from django.contrib import admin
from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class USerProfileAdmin(admin.ModelAdmin):
    # Pomocnicza zmienna (zwykle z podłogą na początku, żeby pokazać, że jest "prywatna")
    _my_fields = ('user', 'email','company', 'phone')
    # Kolumny, które chcemy widzieć w tabeli
    list_display = _my_fields
    # Filtry po prawej stronie ekranu
    list_filter = _my_fields
    # Pasek wyszukiwania!
    search_fields = _my_fields