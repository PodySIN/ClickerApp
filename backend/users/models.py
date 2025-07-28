from django.db import models


class User(models.Model):
    RANK_CHOICES = [
        ('bronze 1', 'Бронза 1'),
        ('bronze 2', 'Бронза 2'),
        ('bronze 3', 'Бронза 3'),
        ('silver 1', 'Серебро 1'),
        ('silver 2', 'Серебро 2'),
        ('silver 3', 'Серебро 3'),
        ('gold 1', 'Золото 1'),
        ('gold 2', 'Золото 2'),
        ('gold 3', 'Золото 3'),
        ('master', 'Мастер'),
        ('elite', 'Элита'),
        ('the_legend', 'Легенда'),
    ]
    id = models.DecimalField(max_digits=15, decimal_places=2, blank=False, default=123456, primary_key=True)
    username = models.CharField(default='username', blank=False)
    level = models.IntegerField(default=1)
    stars = models.FloatField(default=0)
    invited_by = models.IntegerField(default=0)
    energy = models.IntegerField(default=500)
    rank = models.CharField(
        max_length=20,
        choices=RANK_CHOICES,
        default='bronze3'
    )
    last_update = models.DateTimeField(auto_now=True)
