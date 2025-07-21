from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = User(username=validated_data["username"], password=validated_data["password"])
        return user
