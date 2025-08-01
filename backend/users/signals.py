from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import StandartUser
from django.core.cache import cache


@receiver([post_save, post_delete], sender=StandartUser)
def invalidate_level_cache(sender, instance, **kwargs):
    cache.delete_pattern("*user*")
