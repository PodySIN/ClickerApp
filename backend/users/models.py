from django.db import models
from levels.models import Level


class User(models.Model):
    id = models.IntegerField(primary_key=True, default=123456)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True)
    experience = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    current_clicks = models.IntegerField(default=0)
