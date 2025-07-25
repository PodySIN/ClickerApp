from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import LevelSerializer, LevelUpdateSerializer
from .models import Level
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
        summary="Get a list of all levels",
        description="Returns a list of all available levels with their characteristics.",
        parameters=[
            OpenApiParameter(
                name="page_size",
                type=int,
                required=False,
                description="Количество элементов на странице",
                examples=[
                    OpenApiExample(
                        "Example 1",
                        value=10,
                    ),
                ],
            ),
            OpenApiParameter(
                name="sort_by",
                type=str,
                required=False,
                description="Поле для сортировки (например: 'level' или '-click_power')",
                examples=[
                    OpenApiExample(
                        "Example 1",
                        value="level",
                    ),
                ],
            ),
        ],
        responses={
            200: LevelSerializer(many=True),
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример успешного получения списка",
                value={
                    "status": "success",
                    "message": "Уровни успешно получены",
                    "support_data": {
                        "links": {"next": "http://api.example.com/users/?page=2", "previous": None},
                        "count": 100,
                        "page_size": 10,
                    },
                    "data": [
                        {
                            "level": 1,
                            "click_power": 10,
                            "click_capacity": 100,
                            "click_regeneration": 1,
                            "experience_need": 100,
                        },
                        {
                            "level": 1,
                            "click_power": 10,
                            "click_capacity": 100,
                            "click_regeneration": 1,
                            "experience_need": 100,
                        },
                    ],
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Example of a bad response",
                value={
                    "status": "error",
                    "message": "The level was not found",
                },
                response_only=True,
                status_codes=["404"],
            ),
        ],
    ),
    post=extend_schema(
        summary="Create a new level",
        description="Creates a new level with the specified characteristics.",
        request=LevelSerializer,
        responses={
            201: LevelSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Example of a request to create a level",
                value={
                    "level": 1,
                    "click_power": 10,
                    "click_capacity": 100,
                    "click_regeneration": 1,
                    "experience_need": 100,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example of a successful response",
                value={
                    "status": "success",
                    "message": "The level was created successfully",
                    "data": {
                        "level": 1,
                        "click_power": 10,
                        "click_capacity": 100,
                        "click_regeneration": 1,
                        "experience_need": 100,
                    },
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                "Example of a bad response",
                value={
                    "status": "error",
                    "message": "The level was not created",
                    "data": {"level": "level already exists"},
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
)
class LevelListCreateAPIView(APIView):
    """
    API endpoint для получения списка уровней или создания нового уровня.

    Позволяет:
    - GET: получить список всех уровней
    - POST: создать новый уровень
    """

    serializer_class = LevelSerializer

    @method_decorator(cache_page(60 * 15, key_prefix="level_list"))
    def get(self, request) -> Response:
        """
        Получить список всех уровней

        Возвращает JSON-ответ со списком всех уровней и их характеристик.
        Данные кэшируются на 15 минут для повышения производительности.
        """

        sort_by = request.query_params.get("sort_by", "level")
        valid_sort_fields = [
            "level",
            "click_power",
            "click_capacity",
            "click_regeneration",
            "experience_need",
        ]
        if sort_by.lstrip("-") not in valid_sort_fields:
            sort_by = "id"

        levels = get_all_objects_from_model(Level).order_by(sort_by)

        paginator = CustomPageNumberPagination()
        paginator.page_size = request.query_params.get("page_size", 10)
        result_page = paginator.paginate_queryset(levels, request)

        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(
            status="success",
            message="All levels are returned",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request) -> Response:
        """
        Создать новый уровень

        Принимает JSON с характеристиками уровня и создает новую запись.
        Возвращает созданный объект уровня или ошибки валидации.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "The level was created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": "error",
                "message": "The level was not created",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema_view(
    get=extend_schema(
        summary="Get a specific level",
        description="Returns the characteristics of a specific level by its ID.",
        parameters=[
            OpenApiParameter(
                name="level",
                type=int,
                required=True,
                description="ID of the level to receive",
                location=OpenApiParameter.PATH,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        value=1,
                    ),
                    OpenApiExample(
                        "Example 2",
                        value=2,
                    ),
                ],
            )
        ],
        responses={
            200: LevelSerializer,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Example of a successful response",
                value={
                    "status": "success",
                    "message": "The level was successfully obtained",
                    "data": {
                        "level": 1,
                        "click_power": 10,
                        "click_capacity": 100,
                        "click_regeneration": 1,
                        "experience_need": 100,
                    },
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Example of a bad response",
                value={
                    "status": "error",
                    "message": "Level not found",
                },
                response_only=True,
                status_codes=["404"],
            ),
        ],
    ),
    put=extend_schema(
        summary="Full level update",
        description="Completely updates all the characteristics of the level.",
        parameters=[
            OpenApiParameter(
                name="level",
                type=int,
                required=True,
                description="ID уровня для обновления",
                location=OpenApiParameter.PATH,
            )
        ],
        request=LevelSerializer,
        responses={
            200: LevelSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Example of request to update a level",
                value={
                    "level": 1,
                    "click_power": 10,
                    "click_capacity": 100,
                    "click_regeneration": 1,
                    "experience_need": 100,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example of a successful response",
                value={
                    "status": "success",
                    "message": "The level was successfully updated.",
                    "data": {
                        "level": 1,
                        "click_power": 10,
                        "click_capacity": 100,
                        "click_regeneration": 1,
                        "experience_need": 100,
                    },
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Example of a bad response",
                value={
                    "status": "error",
                    "message": "Incorrect data has been entered",
                    "data": {"level": "Level less than one"},
                },
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "Example of a bad response",
                value={
                    "status": "error",
                    "message": "Level not found",
                },
                response_only=True,
                status_codes=["404"],
            ),
        ],
    ),
    patch=extend_schema(
        summary="Partial level upgrade",
        description="Partially updates the level characteristics.",
        parameters=[
            OpenApiParameter(
                name="level",
                type=int,
                required=True,
                description="ID of the upgrade level",
                location=OpenApiParameter.PATH,
            )
        ],
        request=LevelSerializer,
        responses={
            200: LevelSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Example of a successful response",
                value={
                    "level": 1,
                    "click_power": 10,
                    "click_capacity": 100,
                    "click_regeneration": 1,
                    "experience_need": 100,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example of a successful response",
                value={
                    "status": "success",
                    "message": "The level was successfully updated.",
                    "data": {
                        "level": 1,
                        "click_power": 10,
                        "click_capacity": 100,
                        "click_regeneration": 1,
                        "experience_need": 100,
                    },
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Example of a bad response",
                value={
                    "status": "error",
                    "message": "Incorrect data has been entered",
                    "data": {"level": "Level less than one"},
                },
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "Example of a bad response",
                value={
                    "status": "error",
                    "message": "Level not found",
                },
                response_only=True,
                status_codes=["404"],
            ),
        ],
    ),
    delete=extend_schema(
        summary="Delete a level",
        description="Deletes a level by its ID.",
        parameters=[
            OpenApiParameter(
                name="level",
                type=int,
                required=True,
                description="ID of the level to delete",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Example of a bad response",
                value={
                    "status": "error",
                    "message": "the level was successfully deleted",
                    "data": {
                        "level": 1,
                        "click_power": 10,
                        "click_capacity": 100,
                        "click_regeneration": 1,
                        "experience_need": 100,
                    },
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Example of a bad response",
                value={
                    "status": "error",
                    "message": "Level not found",
                },
                response_only=True,
                status_codes=["404"],
            ),
        ],
    ),
)
class LevelRetrieveUpdateAPIView(APIView):
    """
    API endpoint для получения, обновления или удаления конкретного уровня.

    Позволяет:
    - GET: получить конкретный уровень по ID
    - PUT: полное обновление уровня
    - PATCH: частичное обновление уровня
    - DELETE: удаление уровня
    """

    serializer_class = LevelUpdateSerializer

    @method_decorator(cache_page(60 * 15, key_prefix="level_detail"))
    def get(self, request, level: int) -> Response:
        """
        Получить конкретный уровень по ID

        Параметры:
        - level: ID уровня (целое число)

        Возвращает JSON с характеристиками уровня или сообщение об ошибке,
        если уровень не найден. Данные кэшируются на 15 минут.
        """
        level_obj = get_value_from_model(Level, level=level)
        if not level_obj:
            return Response(
                {
                    "status": "error",
                    "message": "Level not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(level_obj)
        return Response(
            {
                "status": "success",
                "message": "The level was found successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, level: int) -> Response:
        """
        Удалить уровень по ID

        Параметры:
        - level: ID уровня для удаления (целое число)

        Возвращает сообщение об успешном удалении или ошибку, если уровень не найден.
        """
        level_obj = get_value_from_model(Level, level=level)
        if not level_obj:
            return Response(
                {
                    "status": "error",
                    "message": "Level not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        level_obj.delete()
        return Response(
            {
                "status": "success",
                "message": "The level was successfully deleted",
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, level: int) -> Response:
        """
        Полное обновление уровня

        Параметры:
        - level: ID уровня для обновления (целое число)
        - request.data: JSON со всеми характеристиками уровня

        Возвращает обновленный объект уровня или ошибки валидации.
        """
        return self._update(request, level, partial=False)

    def patch(self, request, level: int) -> Response:
        """
        Частичное обновление уровня

        Параметры:
        - level: ID уровня для обновления (целое число)
        - request.data: JSON с характеристиками уровня для обновления

        Возвращает обновленный объект уровня или ошибки валидации.
        """
        return self._update(request, level, partial=True)

    def _update(self, request, level: int, partial: bool = False) -> Response:
        """
        Внутренний метод для обработки обновления уровня (PUT/PATCH)

        Параметры:
        - level: ID уровня
        - request: объект запроса
        - partial: флаг частичного обновления

        Возвращает Response с результатом операции
        """
        level_obj = get_value_from_model(Level, level=level)
        if not level_obj:
            return Response(
                {
                    "status": "error",
                    "message": "Level not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(level_obj, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                {
                    "status": "error",
                    "message": "The entered data is incorrect",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "The level was updated successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
