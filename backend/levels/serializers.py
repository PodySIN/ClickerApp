from rest_framework import serializers
from .models import Level


class LevelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Level.

    Обеспечивает:
    - Валидацию полей уровня
    - Создание и обновление уровней
    - Документирование полей для Swagger/OpenAPI
    - Проверку уникальности уровня при создании
    """

    class Meta:
        model = Level
        fields = ["level", "click_power", "click_capacity", "click_regeneration", "experience_need"]
        extra_kwargs = {
            "level": {
                "help_text": "Уникальный номер уровня (целое число >= 1)",
                "label": "Уровень",
                "min_value": 1,
            },
            "click_power": {
                "help_text": "Сила клика (целое число >= 1)",
                "label": "Сила клика",
                "min_value": 1,
            },
            "click_capacity": {
                "help_text": "Максимальное количество кликов (целое число >= 1)",
                "label": "Вместимость",
                "min_value": 1,
            },
            "click_regeneration": {
                "help_text": "Скорость восстановления кликов в секунду (целое число >= 1)",
                "label": "Регенерация",
                "min_value": 1,
            },
            "experience_need": {
                "help_text": "Количество опыта, необходимое для перехода на следующий уровень",
                "label": "Опыт",
                "min_value": 1,
            },
        }

    def validate_level(self, value: int) -> int:
        """Проверяет, что уровень является положительным числом."""
        if value < 1:
            raise serializers.ValidationError("Уровень должен быть положительным числом")
        if Level.objects.filter(level=value).exists():
            raise serializers.ValidationError(
                {"level": f"Уровень с номером {value} уже существует"}
            )
        return value

    def validate_click_power(self, value: int) -> int:
        """Проверяет, что сила клика является положительным числом."""
        if value < 1:
            raise serializers.ValidationError("Сила клика должна быть положительным числом")
        return value

    def validate_click_capacity(self, value: int) -> int:
        """Проверяет, что вместимость кликов является положительным числом."""
        if value < 1:
            raise serializers.ValidationError("Вместимость кликов должна быть положительным числом")
        return value

    def validate_click_regeneration(self, value: int) -> int:
        """Проверяет, что скорость восстановления является положительным числом."""
        if value < 1:
            raise serializers.ValidationError(
                "Скорость восстановления должна быть положительным числом"
            )
        return value

    def validate_experience_need(self, value: int) -> int:
        """Проверяет, что скорость восстановления является положительным числом."""
        if value < 1:
            raise serializers.ValidationError("Количество опыта должно быть положительным числом!")
        return value

    def validate(self, data: dict) -> dict:
        """
        Дополнительная валидация на уровне всего объекта.

        Проверяет логическую согласованность данных:
        - Скорость восстановления не должна превышать вместимость
        """
        click_regeneration = data.get("click_regeneration")
        click_capacity = data.get("click_capacity")

        if click_regeneration and click_capacity and click_regeneration > click_capacity:
            raise serializers.ValidationError(
                "Скорость восстановления не может быть больше вместимости кликов"
            )
        return data

    def create(self, validated_data: dict) -> Level:
        """
        Создает новый уровень с проверкой уникальности номера уровня.

        Args:
            validated_data: Валидированные данные для создания уровня

        Returns:
            Созданный объект Level

        Raises:
            ValidationError: Если уровень с таким номером уже существует
        """

        instance = Level(**validated_data)
        instance.save()
        return instance


class LevelUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Level.

    Обеспечивает:
    - Валидацию полей уровня
    - Создание и обновление уровней
    - Документирование полей для Swagger/OpenAPI
    - Проверку уникальности уровня при создании
    """

    class Meta:
        model = Level
        fields = ["level", "click_power", "click_capacity", "click_regeneration", "experience_need"]
        read_only_fields = ("level",)
        extra_kwargs = {
            "level": {
                "help_text": "Уникальный номер уровня (целое число >= 1)",
                "label": "Уровень",
                "min_value": 1,
            },
            "click_power": {
                "help_text": "Сила клика (целое число >= 1)",
                "label": "Сила клика",
                "min_value": 1,
            },
            "click_capacity": {
                "help_text": "Максимальное количество кликов (целое число >= 1)",
                "label": "Вместимость",
                "min_value": 1,
            },
            "click_regeneration": {
                "help_text": "Скорость восстановления кликов в секунду (целое число >= 1)",
                "label": "Регенерация",
                "min_value": 1,
            },
            "experience_need": {
                "help_text": "Количество опыта, необходимое для перехода на следующий уровень",
                "label": "Опыт",
                "min_value": 1,
            },
        }

    def validate_click_power(self, value: int) -> int:
        """Проверяет, что сила клика является положительным числом."""
        if value < 1:
            raise serializers.ValidationError("Сила клика должна быть положительным числом")
        return value

    def validate_click_capacity(self, value: int) -> int:
        """Проверяет, что вместимость кликов является положительным числом."""
        if value < 1:
            raise serializers.ValidationError("Вместимость кликов должна быть положительным числом")
        return value

    def validate_click_regeneration(self, value: int) -> int:
        """Проверяет, что скорость восстановления является положительным числом."""
        if value < 1:
            raise serializers.ValidationError(
                "Скорость восстановления должна быть положительным числом"
            )
        return value

    def validate_experience_need(self, value: int) -> int:
        """Проверяет, что скорость восстановления является положительным числом."""
        if value < 1:
            raise serializers.ValidationError("Количество опыта должно быть положительным числом!")
        return value

    def validate(self, data: dict) -> dict:
        """
        Дополнительная валидация на уровне всего объекта.

        Проверяет логическую согласованность данных:
        - Скорость восстановления не должна превышать вместимость
        """
        click_regeneration = data.get("click_regeneration")
        click_capacity = data.get("click_capacity")

        if click_regeneration and click_capacity and click_regeneration > click_capacity:
            raise serializers.ValidationError(
                "Скорость восстановления не может быть больше вместимости кликов"
            )
        return data

    def update(self, instance: Level, validated_data: dict) -> Level:
        """
        Обновляет существующий уровень.

        Args:
            instance: Объект Level для обновления
            validated_data: Валидированные данные для обновления

        Returns:
            Обновленный объект Level
        """

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def partial_update(self, instance: Level, validated_data: dict) -> Level:
        """
        Частично обновляет существующий уровень.
        (Алиас для update с partial=True)
        """
        return self.update(instance, validated_data)
