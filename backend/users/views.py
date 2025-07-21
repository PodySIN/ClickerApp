from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
from utils.database_requests import get_value_from_model, get_all_objects_from_model


class UsersAPIView(APIView):

    def get(self, request, id=None):
        if id:
            user = get_value_from_model(User, id=id)
            if user:
                serializer = UserSerializer(user)
                return Response(serializer.data, status=200)
            else:
                return Response({"detail": "Не получилось найти пользователя!"}, status=400)
        else:
            users = get_all_objects_from_model(User)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=200)

    def delete(self, request, id):
        user = get_value_from_model(User, id=id)
        if user:
            user.delete()
            return Response({"detail": "Пользователь успешно удален!"}, status=200)
        else:
            return Response({"detail": "Не получилось найти пользователя!"}, status=400)

    def put(self, request):
        user = get_value_from_model(User, id=id)
        if user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"detail": "Информация пользователя изменена успешно!"}, status=200)
            else:
                return Response({"detail": "Вы ввели неверные данные!"}, status=400)
        else:
            return Response({"detail": "Не получилось найти пользователя!"}, status=400)

    def patch(self, request):
        user = get_value_from_model(User, id=id)
        if user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"detail": "Информация пользователя изменена успешно!"}, status=200)
            else:
                return Response({"detail": "Вы ввели неверные данные!"}, status=400)
        else:
            return Response({"detail": "Не получилось найти пользователя!"}, status=400)
