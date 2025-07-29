from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeNumericFilter
from django.utils.translation import gettext_lazy as _
from .models import Task


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    verbose_name = _("Задачу")
    verbose_name_plural = _("Задачи")

    list_display = ("id", "title", "reward", "short_description")
    list_display_links = ("id", "title")
    list_filter_submit = True
    list_filter = (("reward", RangeNumericFilter),)

    search_fields = ("id", "title", "description")
    search_help_text = _("Поиск по ID, названию или описанию задачи")

    ordering = ("id",)

    fieldsets = (
        (
            None,
            {
                "fields": ("id", "title"),
                "classes": ("wide",),
            },
        ),
        (
            _("Детали задачи"),
            {
                "fields": ("description", "link"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Награда"),
            {
                "fields": ("reward",),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("id",)
        return ()

    def short_description(self, obj):
        """Укорачивает описание для отображения в списке"""
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description

    short_description.short_description = _("Описание")
