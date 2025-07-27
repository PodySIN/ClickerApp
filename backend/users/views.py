from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer, UserUpdateSerializer
from .models import User
from utils.database_requests import get_value_from_model, get_all_objects_from_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    extend_schema_view,
)
from drf_spectacular.types import OpenApiTypes
from utils.paginators import CustomPageNumberPagination


@extend_schema_view(
    get=extend_schema(
        summary="Получить список пользователей",
        description="Возвращает список всех пользователей с возможностью фильтрации, сортировки и пагинации.",
        parameters=[
            OpenApiParameter(
                name="username",
                type=str,
                required=False,
                description="Фильтр по имени пользователя (регистронезависимый поиск по подстроке)",
                examples=[
                    OpenApiExample("Пример 1", value="john"),
                    OpenApiExample("Пример 2", value="alice"),
                ],
            ),
            OpenApiParameter(
                name="invited_by",
                type=int,
                required=False,
                description="Фильтр по ID пользователя, который пригласил",
                examples=[
                    OpenApiExample("Пример 1", value=123456),
                    OpenApiExample("Пример 2", value=654321),
                ],
            ),
            OpenApiParameter(
                name="rank",
                type=str,
                required=False,
                description="Фильтр по рангу пользователя",
                examples=[
                    OpenApiExample("Пример 1", value="silver1"),
                    OpenApiExample("Пример 2", value="gold3"),
                ],
            ),
            OpenApiParameter(
                name="sort_by",
                type=str,
                required=False,
                description="Поле для сортировки (- для обратного порядка)",
                examples=[
                    OpenApiExample("По уровню", value="level"),
                    OpenApiExample("По звездам (убывание)", value="-stars"),
                    OpenApiExample("По энергии", value="energy"),
                ],
            ),
            OpenApiParameter(
                name="page_size",
                type=int,
                required=False,
                description="Количество пользователей на странице",
                examples=[
                    OpenApiExample("10 пользователей", value=10),
                    OpenApiExample("20 пользователей", value=20),
                ],
            ),
        ],
        responses={
            200: UserSerializer(many=True),
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "status": "success",
                    "message": "Пользователи успешно получены",
                    "support_data": {
                        "links": {
                            "next": "http://api.example.com/users/?page=2&page_size=10",
                            "previous": None,
                        },
                        "count": 150,
                        "page_size": 10,
                    },
                    "data": [
                        {
                            "id": 123456789,
                            "username": "john_doe",
                            "level": 5,
                            "stars": 150.5,
                            "invited_by": 987654321,
                            "energy": 200,
                            "rank": "silver1",
                        },
                        {
                            "id": 987654321,
                            "username": "alice_smith",
                            "level": 8,
                            "stars": 320.0,
                            "invited_by": 0,
                            "energy": 350,
                            "rank": "gold3",
                        },
                    ],
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример ошибки валидации",
                value={
                    "status": "error",
                    "message": "Ошибка валидации",
                    "data": {"rank": ["Неверное значение ранга"]},
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
    post=extend_schema(
        summary="Создать нового пользователя",
        description="Создает нового пользователя с указанными характеристиками.",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример запроса на создание",
                value={
                    "id": 123456789,
                    "username": "new_user",
                    "level": 1,
                    "stars": 0.0,
                    "invited_by": 987654321,
                    "energy": 500,
                    "rank": "bronze3",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Пример успешного создания",
                value={
                    "status": "success",
                    "message": "Пользователь успешно создан",
                    "data": {
                        "id": 123456789,
                        "username": "new_user",
                        "level": 1,
                        "stars": 0.0,
                        "invited_by": 987654321,
                        "energy": 500,
                        "rank": "bronze3",
                    },
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                "Пример ошибки (неверный ранг)",
                value={
                    "status": "error",
                    "message": "Ошибка валидации",
                    "data": {"rank": ["Неверное значение ранга"]},
                },
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "Пример ошибки (пользователь существует)",
                value={
                    "status": "error",
                    "message": "Ошибка создания пользователя",
                    "data": {"id": ["Пользователь с таким id: 123456789, уже существует"]},
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
)
class UserListCreateAPIView(APIView):
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination

    @method_decorator(cache_page(60 * 15, key_prefix="user_list"))
    def get(self, request):
        queryset = get_all_objects_from_model(User)
        # Фильтрация
        if username := request.query_params.get("username"):
            queryset = queryset.filter(username__icontains=username)
        if invited_by := request.query_params.get("invited_by"):
            queryset = queryset.filter(invited_by=invited_by)
        if rank := request.query_params.get("rank"):
            queryset = queryset.filter(rank=rank.lower())
        
        # Сортировка
        sort_by = request.query_params.get("sort_by", "id")
        valid_sort_fields = ["id", "username", "level", "stars", "invited_by", "energy", "rank"]
        if sort_by.lstrip("-") in valid_sort_fields:
            queryset = queryset.order_by(sort_by)

        # Пагинация
        paginator = self.pagination_class()
        paginator.page_size = request.query_params.get("page_size", 10)
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(
            status="success",
            message="Пользователи успешно получены",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Пользователь успешно создан",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": "error",
                "message": "Ошибка создания пользователя",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema_view(
    get=extend_schema(
        summary="Получить пользователя по ID",
        description="Возвращает данные конкретного пользователя по его ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                required=True,
                description="ID пользователя (Telegram ID)",
                location=OpenApiParameter.PATH,
                examples=[
                    OpenApiExample("Пример 1", value=123456789),
                    OpenApiExample("Пример 2", value=987654321),
                ],
            )
        ],
        responses={
            200: UserSerializer,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "status": "success",
                    "message": "Пользователь успешно получен",
                    "data": {
                        "id": 123456789,
                        "username": "john_doe",
                        "level": 5,
                        "stars": 150.5,
                        "invited_by": 987654321,
                        "energy": 200,
                        "rank": "silver1",
                    },
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример ошибки (не найден)",
                value={
                    "status": "error",
                    "message": "Пользователь не найден",
                },
                response_only=True,
                status_codes=["404"],
            ),
        ],
    ),
    put=extend_schema(
        summary="Полное обновление пользователя",
        description="Полностью обновляет все данные пользователя. Обязательны все поля.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                required=True,
                description="ID пользователя для обновления",
                location=OpenApiParameter.PATH,
                examples=[OpenApiExample("Пример", value=123456789)],
            )
        ],
        request=UserUpdateSerializer,
        responses={
            200: UserUpdateSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "username": "updated_user",
                    "level": 6,
                    "stars": 200.0,
                    "invited_by": 0,
                    "energy": 300,
                    "rank": "silver2",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "status": "success",
                    "message": "Данные пользователя успешно обновлены",
                    "data": {
                        "id": 123456789,
                        "username": "updated_user",
                        "level": 6,
                        "stars": 200.0,
                        "invited_by": 0,
                        "energy": 300,
                        "rank": "silver2",
                    },
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример ошибки валидации",
                value={
                    "status": "error",
                    "message": "Ошибка валидации",
                    "data": {
                        "level": ["level должен быть положительным числом"],
                        "rank": ["Неверное значение ранга"],
                    },
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
    patch=extend_schema(
        summary="Частичное обновление пользователя",
        description="Обновляет только указанные поля пользователя.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                required=True,
                description="ID пользователя для обновления",
                location=OpenApiParameter.PATH,
                examples=[OpenApiExample("Пример", value=123456789)],
            )
        ],
        request=UserUpdateSerializer,
        responses={
            200: UserUpdateSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример запроса (обновление только уровня и энергии)",
                value={
                    "level": 7,
                    "energy": 400,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "status": "success",
                    "message": "Данные пользователя успешно обновлены",
                    "data": {
                        "id": 123456789,
                        "username": "updated_user",
                        "level": 7,
                        "stars": 200.0,
                        "invited_by": 0,
                        "energy": 400,
                        "rank": "silver2",
                    },
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример ошибки (неверный invited_by)",
                value={
                    "status": "error",
                    "message": "Ошибка валидации",
                    "data": {
                        "invited_by": ["Пользователь с id 999999 не существует"],
                    },
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
    delete=extend_schema(
        summary="Удалить пользователя",
        description="Удаляет пользователя по ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                required=True,
                description="ID пользователя для удаления",
                location=OpenApiParameter.PATH,
                examples=[OpenApiExample("Пример", value=123456789)],
            )
        ],
        responses={
            204: None,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример успешного удаления",
                value=None,
                response_only=True,
                status_codes=["204"],
            ),
            OpenApiExample(
                "Пример ошибки (не найден)",
                value={
                    "status": "error",
                    "message": "Пользователь не найден",
                },
                response_only=True,
                status_codes=["404"],
            ),
        ],
    ),
)
class UserRetrieveUpdateAPIView(APIView):
    serializer_class = UserUpdateSerializer

    @method_decorator(cache_page(60 * 15, key_prefix="user_detail"))
    def get(self, request, id):
        user = get_value_from_model(User, id=id)
        if not user:
            return Response(
                {"status": "error", "message": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(user)
        return Response(
            {
                "status": "success",
                "message": "Пользователь успешно получен",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, id):
        return self._update(request, id, partial=False)

    def patch(self, request, id):
        return self._update(request, id, partial=True)

    def delete(self, request, id):
        user = get_value_from_model(User, id=id)
        if not user:
            return Response(
                {"status": "error", "message": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update(self, request, id, partial=False):
        user = get_value_from_model(User, id=id)
        if not user:
            return Response(
                {"status": "error", "message": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            user, 
            data=request.data, 
            partial=partial
        )

        if not serializer.is_valid():
            return Response(
                {
                    "status": "error", 
                    "message": "Ошибка валидации", 
                    "data": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "Данные пользователя успешно обновлены",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )