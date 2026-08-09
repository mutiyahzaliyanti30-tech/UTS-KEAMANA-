from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def buat_profile_otomatis(sender, instance, created, **kwargs):
    """
    Setiap kali ada User baru dibuat (termasuk lewat createsuperuser),
    otomatis dibuatkan Profile dengan role default 'user'.
    Ini mencegah ada User yang 'yatim' tanpa role.
    """
    if created:
        Profile.objects.get_or_create(user=instance)
