from django.db import models


class Level(models.Model):
    level = models.IntegerField(default=1, primary_key=True)
    click_power = models.IntegerField(default=1)
    click_capacity = models.IntegerField(default=100)
    click_regeneration = models.IntegerField(default=1)
    experience_need = models.IntegerField(default=100)
