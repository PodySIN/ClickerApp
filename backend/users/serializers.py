from rest_framework import serializers
from .models import User
from levels.models import Level


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "level", "experience", "stars", "current_clicks"]
        extra_kwargs = {
            "id": {
                "help_text": "Уникальный id пользователя (телеграмм id)",
                "label": "id",
                "min_value": 1,
            },
            "level": {
                "help_text": "Уровень пользователя",
                "label": "Level",
            },
            "experience": {
                "help_text": "Количество опыта пользователя",
                "label": "Experience",
                "min_value": 1,
            },
            "stars": {
                "help_text": "Количество звезд у пользователя (валюты)",
                "label": "Stars",
                "min_value": 1,
            },
            "current_clicks": {
                "help_text": "Количество кликов по звездочке в данный момент",
                "label": "Clicks",
                "min_value": 1,
            },
        }

    def validate_id(self, value: int) -> int:
        """Проверяет, что id является положительным числом."""
        if value < 1:
            raise serializers.ValidationError("id должен быть положительным числом")
        if User.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                {"level": f"Пользователь с таким id: {value}, уже существует"}
            )
        return value

    def validate_level(self, value: Level) -> int:
        """Проверяет, что level является положительным числом."""
        if value.level < 1:
            raise serializers.ValidationError("level должен быть положительным числом")
        return value

    def validate_experience(self, value: int) -> int:
        """Проверяет, что experience является положительным числом."""
        if value < 0:
            raise serializers.ValidationError("experience должен быть положительным числом")
        return value

    def validate_stars(self, value: int) -> int:
        """Проверяет, что звезды пользователя являются положительным числом."""
        if value < 0:
            raise serializers.ValidationError(
                "Звезды пользователя должны быть положительным числом"
            )
        return value

    def validate_current_clicks(self, value: int) -> int:
        """Проверяет, что current_clicks является положительным числом."""
        if value < 0:
            raise serializers.ValidationError("Сurrent_clicks должно быть положительным числом!")
        return value

    def create(self, validated_data: dict) -> User:
        """
        Создает нового пользователя с проверкой уникальности номера уровня.

        Args:
            validated_data: Валидированные данные для создания уровня

        Returns:
            Созданный объект User

        Raises:
            ValidationError: Если пользователь с таким номером уже существует
        """

        instance = User(**validated_data)
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "level", "experience", "stars", "current_clicks"]
        read_only_fields = ("id",)
        extra_kwargs = {
            "level": {
                "help_text": "Уровень пользователя",
                "label": "Level",
            },
            "experience": {
                "help_text": "Количество опыта пользователя",
                "label": "Experience",
                "min_value": 1,
            },
            "stars": {
                "help_text": "Количество звезд у пользователя (валюты)",
                "label": "Stars",
                "min_value": 1,
            },
            "current_clicks": {
                "help_text": "Количество кликов по звездочке в данный момент",
                "label": "Clicks",
                "min_value": 1,
            },
        }

    def validate_level(self, value: Level) -> int:
        """Проверяет, что level является положительным числом."""
        if value.level < 1:
            raise serializers.ValidationError("level должен быть положительным числом")
        return value

    def validate_experience(self, value: int) -> int:
        """Проверяет, что experience является положительным числом."""
        if value < 0:
            raise serializers.ValidationError("experience должен быть положительным числом")
        return value

    def validate_stars(self, value: int) -> int:
        """Проверяет, что звезды пользователя являются положительным числом."""
        if value < 0:
            raise serializers.ValidationError(
                "Звезды пользователя должны быть положительным числом"
            )
        return value

    def validate_current_clicks(self, value: int) -> int:
        """Проверяет, что current_clicks является положительным числом."""
        if value < 0:
            raise serializers.ValidationError("Сurrent_clicks должно быть положительным числом!")
        return value

    def update(self, instance: User, validated_data: dict) -> User:
        """
        Обновляет существующего пользователя.

        Args:
            instance: Объект User для обновления
            validated_data: Валидированные данные для обновления

        Returns:
            Обновленный объект User
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def partial_update(self, instance: User, validated_data: dict) -> User:
        """
        Частично обновляет существующего пользователя.
        (Алиас для update с partial=True)
        """
        return self.update(instance, validated_data)
