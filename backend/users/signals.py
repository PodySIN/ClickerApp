from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User
from django.core.cache import cache


@receiver([post_save, post_delete], sender=User)
def invalidate_level_cache(sender, instance, **kwargs):
    print('now_celery_clear_cache')
    cache.delete_pattern("*user*")
