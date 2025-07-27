from django.db import models


class User(models.Model):
    RANK_CHOICES = [
        ('bronze1', 'Бронза 1'),
        ('bronze2', 'Бронза 2'),
        ('bronze3', 'Бронза 3'),
        ('silver1', 'Серебро 1'),
        ('silver2', 'Серебро 2'),
        ('silver3', 'Серебро 3'),
        ('gold1', 'Золото 1'),
        ('gold2', 'Золото 2'),
        ('gold3', 'Золото 3'),
        ('master', 'Мастер'),
        ('elite', 'Элита'),
        ('the_legend', 'Легенда'),
    ]
    id = models.IntegerField(primary_key=True, default=123456)
    username = models.CharField(default='')
    level = models.IntegerField(default=1)
    stars = models.FloatField(default=0)
    invited_by = models.IntegerField(default=0)
    energy = models.IntegerField(default=500)
    rank = models.CharField(
        max_length=20,
        choices=RANK_CHOICES,
        default='bronze3'
    )
