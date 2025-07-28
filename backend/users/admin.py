from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeNumericFilter
from .models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    # Список полей в таблице
    list_display = ("id", "username", "level", "stars", "rank", "energy", "last_update")
    list_display_links = ("id", "username")  # Кликабельные поля

    # Фильтры (с поддержкой unfold)
    list_filter = (
        "rank",
        ("level", RangeNumericFilter),  # Числовой диапазон
        ("energy", RangeNumericFilter),
    )

    # Поиск
    search_fields = ("id", "username", "invited_by")
    search_help_text = "Поиск по ID, имени или ID пригласившего"

    # Сортировка
    ordering = ("-last_update",)

    # Группировка полей в форме редактирования
    fieldsets = (
        (
            None,
            {
                "fields": ("id", "username", "last_update"),
                "classes": ("wide",),
            },
        ),
        (
            "Прогресс",
            {
                "fields": ("level", "stars", "rank"),
                "classes": ("collapse",),
            },
        ),
        (
            "Энергия и рефералы",
            {
                "fields": ("energy", "invited_by"),
            },
        ),
    )

    # Только для чтения при редактировании
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Если объект уже существует
            return ("id", "last_update")
        return ("last_update",)

    # Кастомизация действий в списке
    actions = ["reset_energy"]

    @admin.action(description="Обнулить энергию")
    def reset_energy(self, request, queryset):
        queryset.update(energy=0)
        self.message_user(request, f"Энергия обнулена для {queryset.count()} пользователей")
