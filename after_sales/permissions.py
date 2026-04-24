def can_create_update_ticket(user):
    # Funkcja zwraca True, jeśli użytkownik jest w grupie "CreateUpdateTicket" (lub jest superadminem)
    return user.groups.filter(name='CreateUpdateTicket').exists() or user.is_superuser