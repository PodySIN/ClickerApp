from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Level
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Level)
def invalidate_level_cache(sender, instance, **kwargs):
    cache.delete_pattern("*level*")
