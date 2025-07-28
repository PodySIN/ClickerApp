from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "level", "stars", "invited_by", "energy", "rank", "last_update"]
        extra_kwargs = {
            "id": {
                "help_text": "Уникальный id пользователя (телеграмм id)",
                "label": "id",
                "min_value": 1,
            },
            "username": {
                "help_text": "Имя пользователя",
                "label": "Username",
                "max_length": 100,
            },
            "level": {
                "help_text": "Уровень пользователя",
                "label": "Level",
                "min_value": 1,
            },
            "stars": {
                "help_text": "Количество звезд у пользователя (валюты)",
                "label": "Stars",
                "min_value": 0,
            },
            "invited_by": {
                "help_text": "ID пользователя, который пригласил",
                "label": "Invited By",
                "min_value": 0,
            },
            "energy": {
                "help_text": "Количество энергии пользователя",
                "label": "Energy",
                "min_value": 0,
            },
            "rank": {
                "help_text": "Ранг пользователя (bronze3, silver1 и т.д.)",
                "label": "Rank",
            },
            "last_update": {
                "help_text": "Время, когда пользователя бы изменен последний раз",
                "label": "Last Update",
            },
        }
        read_only_fields = ("last_update",)

    def validate_id(self, value: int) -> int:
        if value < 1:
            raise serializers.ValidationError("id должен быть положительным числом")
        if User.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Пользователь с таким id: {value}, уже существует")
        return value

    def validate_level(self, value: int) -> int:
        if value < 1:
            raise serializers.ValidationError("level должен быть положительным числом")
        return value

    def validate_stars(self, value: float) -> float:
        if value < 0:
            raise serializers.ValidationError(
                "Звезды пользователя должны быть неотрицательным числом"
            )
        return value

    def validate_invited_by(self, value: int) -> int:
        if value < 0:
            raise serializers.ValidationError("ID пригласившего должен быть неотрицательным числом")
        if value != 0 and not User.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                f"Пользователь с id {value} (пригласивший) не существует"
            )
        return value

    def validate_energy(self, value: int) -> int:
        if value < 0:
            raise serializers.ValidationError("Energy должно быть неотрицательным числом")
        return value

    def validate_rank(self, value):
        valid_ranks = [choice[0] for choice in User.RANK_CHOICES]
        if value not in valid_ranks:
            raise serializers.ValidationError("Неверное значение ранга")
        return value

    def create(self, validated_data: dict) -> User:
        instance = User(**validated_data)
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "level", "stars", "invited_by", "energy", "rank", "last_update"]
        read_only_fields = ("id",)
        extra_kwargs = {
            "username": {"max_length": 100},
            "level": {"min_value": 1},
            "stars": {"min_value": 0},
            "invited_by": {"min_value": 0},
            "energy": {"min_value": 0},
        }
        read_only_fields = ("last_update",)

    def validate(self, data):
        # Проверка invited_by при обновлении
        if "invited_by" in data and data["invited_by"] != 0:
            if not User.objects.filter(id=data["invited_by"]).exists():
                raise serializers.ValidationError(
                    {"invited_by": f"Пользователь с id {data['invited_by']} не существует"}
                )
        return data

    def update(self, instance: User, validated_data: dict) -> User:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class AdminCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        min_length=8,
        help_text="Пароль должен быть не менее 8 символов",
    )
    password2 = serializers.CharField(
        write_only=True, style={"input_type": "password"}, help_text="Повторите тот же пароль"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {"email": {"required": True}, "username": {"min_length": 3}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError(
                {"username": "Пользователь с таким именем уже существует"}
            )

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"email": "Пользователь с таким email уже существует"}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=make_password(validated_data["password"]),
            is_staff=True,
            is_superuser=True,
        )
        return user
