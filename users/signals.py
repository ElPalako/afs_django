from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def notify_user_activation(sender, instance, created, **kwargs):
    # Sprawdzamy, czy to nie jest nowo utworzony użytkownik (bo on jest nieaktywny)
    # oraz czy flaga is_active właśnie została ustawiona na True
    if not created and instance.is_active:
        # Tu wpiszemy logikę wysyłki maila
        print(f"Wysyłam maila do {instance.email}: Twoje konto jest już aktywne!")
        
        # Zakładając, że masz skonfigurowany serwer SMTP w settings.py:
        # send_mail(
        #     'Konto AfterSales Pro aktywne!',
        #     'Cześć! Twoje konto zostało właśnie aktywowane przez admina. Możesz się zalogować.',
        #     'admin@aftersales.pro',
        #     [instance.email],
        #     fail_silently=False,
        # )