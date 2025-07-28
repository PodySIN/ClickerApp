from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeNumericFilter, RangeDateTimeFilter
from django.utils.translation import gettext_lazy as _
from .models import StandartUser
from unfold.decorators import action


@admin.register(StandartUser)
class UserAdmin(ModelAdmin):

    verbose_name = _("Пользователя")
    verbose_name_plural = _("Пользователи")

    list_display = ("id", "username", "level", "stars", "rank", "energy", "last_update")
    list_display_links = ("id", "username")
    list_filter_submit = True
    list_filter = (
        "rank",
        ("level", RangeNumericFilter),
        ("stars", RangeNumericFilter),
        ("energy", RangeNumericFilter),
        ("last_update", RangeDateTimeFilter),
    )

    search_fields = ("id", "username", "invited_by")
    search_help_text = _("Поиск по ID, имени или ID пригласившего")  # Перевод подсказки

    ordering = ("id",)

    fieldsets = (
        (
            None,
            {
                "fields": ("id", "username", "last_update"),
                "classes": ("wide",),
            },
        ),
        (
            _("Прогресс"),  # Перевод названия секции
            {
                "fields": ("level", "stars", "rank"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Энергия и рефералы"),
            {
                "fields": ("energy", "invited_by"),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("id", "last_update")
        return ("last_update",)
