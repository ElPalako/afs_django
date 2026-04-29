def can_create_update_order(user):
    # Funkcja zwraca True, jeśli użytkownik jest w grupie "CreateUpdateOrder" (lub jest superadminem)
    return user.groups.filter(name='CreateUpdateOrder').exists() or user.is_superuser