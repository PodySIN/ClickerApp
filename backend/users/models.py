from django.db import models
from django.utils.translation import gettext_lazy as _  # Импорт для перевода


class StandartUser(models.Model):
    RANK_CHOICES = [
        ("bronze 1", "Бронза 1"),
        ("bronze 2", "Бронза 2"),
        ("bronze 3", "Бронза 3"),
        ("silver 1", "Серебро 1"),
        ("silver 2", "Серебро 2"),
        ("silver 3", "Серебро 3"),
        ("gold 1", "Золото 1"),
        ("gold 2", "Золото 2"),
        ("gold 3", "Золото 3"),
        ("master", "Мастер"),
        ("elite", "Элита"),
        ("the_legend", "Легенда"),
    ]

    id = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        blank=False,
        default=123456,
        primary_key=True,
        verbose_name=_("ID пользователя"),  # Перевод названия поля
    )
    username = models.CharField(
        default="username",
        blank=False,
        verbose_name=_("Имя пользователя"),
    )
    level = models.IntegerField(
        default=1,
        verbose_name=_("Уровень"),
    )
    stars = models.FloatField(
        default=0,
        verbose_name=_("Звёзды"),
    )
    invited_by = models.IntegerField(
        default=0,
        verbose_name=_("Пригласил (ID)"),
    )
    energy = models.IntegerField(
        default=500,
        verbose_name=_("Энергия"),
    )
    rank = models.CharField(
        choices=RANK_CHOICES,
        default="bronze3",
        verbose_name=_("Ранг"),
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Последнее обновление"),
    )

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return self.username
