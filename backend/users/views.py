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
        summary="Получить список пользователей или конкретного пользователя",
        description="Возвращает список всех пользователей или конкретного пользователя по ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                required=False,
                description="ID пользователя (Telegram ID)",
                examples=[
                    OpenApiExample("Пример ID пользователя", value=123456789),
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
            OpenApiParameter(
                name="sort_by",
                type=str,
                required=False,
                description="Поле для сортировки (- для обратного порядка)",
                examples=[
                    OpenApiExample("Сортировка по уровню", value="level"),
                    OpenApiExample("Сортировка по опыту (по убыванию)", value="-experience"),
                ],
            ),
        ],
        responses={
            200: UserSerializer(many=True),
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример успешного получения списка",
                value={
                    "status": "success",
                    "message": "Пользователи успешно получены",
                    "support_data": {
                        "links": {"next": "http://api.example.com/users/?page=2", "previous": None},
                        "count": 100,
                        "page_size": 10,
                    },
                    "data": [
                        {
                            "id": 123456789,
                            "level": 5,
                            "experience": 1200,
                            "stars": 50,
                            "current_clicks": 10,
                        },
                        {
                            "id": 987654321,
                            "level": 3,
                            "experience": 800,
                            "stars": 30,
                            "current_clicks": 5,
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
                    "data": {"id": ["Пользователь с таким ID уже существует"]},
                },
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "Пример ошибки (пользователь не найден)",
                value={"status": "error", "message": "Пользователь не найден"},
                response_only=True,
                status_codes=["404"],
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
                    "level": 1,
                    "experience": 0,
                    "stars": 0,
                    "current_clicks": 0,
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
                        "level": 1,
                        "experience": 0,
                        "stars": 0,
                        "current_clicks": 0,
                    },
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                "Пример ошибки валидации",
                value={
                    "status": "error",
                    "message": "Ошибка валидации",
                    "data": {"id": ["Пользователь с таким ID уже существует"]},
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
)
class UserListCreateAPIView(APIView):
    """API для работы с пользователями: получение списка и создание"""

    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination

    @method_decorator(cache_page(60 * 15, key_prefix="user"))
    def get(self, request):
        """
        Получить список всех пользователей

        Возвращает JSON-ответ со списком всех уровней и их характеристик.
        Данные кэшируются на 15 минут для повышения производительности.
        """

        sort_by = request.query_params.get("sort_by", "id")
        valid_sort_fields = ["id", "level", "experience", "stars", "current_clicks"]

        if sort_by.lstrip("-") not in valid_sort_fields:
            sort_by = "id"

        users = get_all_objects_from_model(User).order_by(sort_by)

        paginator = self.pagination_class()
        paginator.page_size = request.query_params.get("page_size", 10)
        result_page = paginator.paginate_queryset(users, request)

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
        summary="Получить конкретного пользователя",
        description="Возвращает данные конкретного пользователя по ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                required=True,
                description="ID пользователя (Telegram ID)",
                location=OpenApiParameter.PATH,
                examples=[OpenApiExample("Пример ID", value=123456789)],
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
                        "level": 5,
                        "experience": 1200,
                        "stars": 50,
                        "current_clicks": 10,
                    },
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример ошибки",
                value={"status": "error", "message": "Пользователь не найден"},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    ),
    put=extend_schema(
        summary="Полное обновление пользователя",
        description="Полностью обновляет все данные пользователя.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                required=True,
                description="ID пользователя для обновления",
                location=OpenApiParameter.PATH,
            )
        ],
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={"level": 5, "experience": 1200, "stars": 50, "current_clicks": 10},
                request_only=True,
            ),
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "status": "success",
                    "message": "Данные пользователя успешно обновлены",
                    "data": {
                        "id": 123456789,
                        "level": 5,
                        "experience": 1200,
                        "stars": 50,
                        "current_clicks": 10,
                    },
                },
                response_only=True,
                status_codes=["200"],
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
            )
        ],
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={"experience": 1500, "stars": 60},
                request_only=True,
            ),
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "status": "success",
                    "message": "Данные пользователя успешно обновлены",
                    "data": {
                        "id": 123456789,
                        "level": 5,
                        "experience": 1500,
                        "stars": 60,
                        "current_clicks": 10,
                    },
                },
                response_only=True,
                status_codes=["200"],
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
            )
        ],
        responses={
            200: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                value={"status": "success", "message": "Пользователь успешно удален"},
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
)
class UserRetrieveUpdateAPIView(APIView):
    """API для работы с конкретным пользователем: получение, обновление, удаление"""

    serializer_class = UserUpdateSerializer

    @method_decorator(cache_page(60 * 15, key_prefix="user"))
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
        return Response(
            {"status": "success", "message": "Пользователь успешно удален"},
            status=status.HTTP_200_OK,
        )

    def _update(self, request, id, partial=False):
        user = get_value_from_model(User, id=id)
        if not user:
            return Response(
                {"status": "error", "message": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(user, data=request.data, partial=partial)

        if not serializer.is_valid():
            return Response(
                {"status": "error", "message": "Ошибка валидации", "data": serializer.errors},
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
