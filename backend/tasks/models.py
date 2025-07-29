from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи", blank=True, null=True)
    link = models.URLField(verbose_name="Ссылка", blank=True, null=True)
    reward = models.IntegerField(verbose_name="Награда", default=0)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title
