from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "link", "reward"]
        extra_kwargs = {
            "id": {
                "help_text": "Уникальный id задачи",
                "label": "id",
                "read_only": True,
            },
            "title": {
                "help_text": "Название задачи",
                "label": "Title",
                "max_length": 200,
                "required": True,
            },
            "description": {
                "help_text": "Подробное описание задачи",
                "label": "Description",
                "required": False,
                "allow_blank": True,
            },
            "link": {
                "help_text": "Ссылка на задачу",
                "label": "Link",
                "required": False,
                "allow_blank": True,
            },
            "reward": {
                "help_text": "Награда за выполнение задачи",
                "label": "Reward",
                "min_value": 0,
                "default": 0,
            },
        }

    def validate_title(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Название задачи не может быть пустым")
        return value

    def validate_reward(self, value: int) -> int:
        if value < 0:
            raise serializers.ValidationError("Награда не может быть отрицательной")
        return value

    def create(self, validated_data: dict) -> Task:
        return Task.objects.create(**validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "link", "reward"]
        read_only_fields = ("id",)
        extra_kwargs = {
            "title": {"max_length": 200, "required": False},
            "description": {"required": False, "allow_blank": True},
            "link": {"required": False, "allow_blank": True},
            "reward": {"min_value": 0, "required": False},
        }

    def update(self, instance: Task, validated_data: dict) -> Task:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
