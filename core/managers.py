from django.db import models

class BaseCompanyManager(models.Manager):
    """
    Niestandardowy Manager, który filtruje zapytania na podstawie firmy użytkownika.
    Zaprojektowany tak, aby działał z każdym modelem, który ma pole 'business_partner'.
    """
    def for_user(self, user):
        # 1. Pobieramy domyślne zapytanie (czyli tak jakbyśmy zrobili .all())
        queryset = super().get_queryset()
        
        # 2. Sprawdzamy, czy to administrator lub "nasz" pracownik (bez przypisanej firmy)
        if user.is_superuser or user.profile.company is None:
            # Jeśli tak, oddajemy mu wszystko (czysty queryset)
            return queryset
            
        # 3. Jeśli to klient (ma przypisaną firmę), filtrujemy dane twardo po jego firmie
        # Zabezpiecza nas to przed wyciekiem danych innych klientów
        return queryset.filter(business_partner=user.profile.company)