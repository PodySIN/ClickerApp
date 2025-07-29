from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import TaskSerializer, TaskUpdateSerializer
from .models import Task
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
        summary="Получить список задач",
        description="Возвращает список всех задач с возможностью фильтрации и пагинации.",
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                required=False,
                description="Фильтр по названию задачи (регистронезависимый поиск по подстроке)",
                examples=[
                    OpenApiExample("Пример 1", value="важная"),
                    OpenApiExample("Пример 2", value="срочная"),
                ],
            ),
            OpenApiParameter(
                name="min_reward",
                type=int,
                required=False,
                description="Фильтр по минимальной награде",
                examples=[
                    OpenApiExample("От 100", value=100),
                    OpenApiExample("От 500", value=500),
                ],
            ),
            OpenApiParameter(
                name="sort_by",
                type=str,
                required=False,
                description="Поле для сортировки (- для обратного порядка)",
                examples=[
                    OpenApiExample("По награде", value="reward"),
                    OpenApiExample("По названию (убывание)", value="-title"),
                ],
            ),
            OpenApiParameter(
                name="page_size",
                type=int,
                required=False,
                description="Количество задач на странице",
                examples=[
                    OpenApiExample("10 задач", value=10),
                    OpenApiExample("20 задач", value=20),
                ],
            ),
        ],
        responses={
            200: TaskSerializer(many=True),
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "status": "success",
                    "message": "Задачи успешно получены",
                    "support_data": {
                        "links": {
                            "next": "http://api.example.com/tasks/?page=2&page_size=10",
                            "previous": None,
                        },
                        "count": 50,
                        "page_size": 10,
                    },
                    "data": [
                        {
                            "id": 1,
                            "title": "Важная задача",
                            "description": "Выполнить срочное задание",
                            "link": "https://example.com/task1",
                            "reward": 500,
                        },
                        {
                            "id": 2,
                            "title": "Обычная задача",
                            "description": "Рутинная работа",
                            "link": "",
                            "reward": 100,
                        },
                    ],
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
    post=extend_schema(
        summary="Создать новую задачу",
        description="Создает новую задачу с указанными параметрами.",
        request=TaskSerializer,
        responses={
            201: TaskSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Пример запроса на создание",
                value={
                    "title": "Новая задача",
                    "description": "Описание новой задачи",
                    "link": "https://example.com/new-task",
                    "reward": 300,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Пример успешного создания",
                value={
                    "status": "success",
                    "message": "Задача успешно создана",
                    "data": {
                        "id": 3,
                        "title": "Новая задача",
                        "description": "Описание новой задачи",
                        "link": "https://example.com/new-task",
                        "reward": 300,
                    },
                },
                response_only=True,
                status_codes=["201"],
            ),
        ],
    ),
)
class TaskListCreateAPIView(APIView):
    serializer_class = TaskSerializer
    pagination_class = CustomPageNumberPagination

    @method_decorator(cache_page(60 * 15, key_prefix="task"))
    def get(self, request):
        queryset = Task.objects.all()

        # Фильтрация
        if title := request.query_params.get("title"):
            queryset = queryset.filter(title__icontains=title)
        if min_reward := request.query_params.get("min_reward"):
            queryset = queryset.filter(reward__gte=min_reward)

        # Сортировка
        sort_by = request.query_params.get("sort_by", "id")
        valid_sort_fields = ["id", "title", "reward"]
        if sort_by.lstrip("-") in valid_sort_fields:
            queryset = queryset.order_by(sort_by)

        # Пагинация
        paginator = self.pagination_class()
        paginator.page_size = request.query_params.get("page_size", 10)
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(
            status="success",
            message="Задачи успешно получены",
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
                    "message": "Задача успешно создана",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": "error",
                "message": "Ошибка создания задачи",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema_view(
    get=extend_schema(
        summary="Получить задачу по ID",
        description="Возвращает данные конкретной задачи по её ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                required=True,
                description="ID задачи",
                location=OpenApiParameter.PATH,
                examples=[
                    OpenApiExample("Пример 1", value=1),
                    OpenApiExample("Пример 2", value=2),
                ],
            )
        ],
        responses={
            200: TaskSerializer,
            404: OpenApiTypes.OBJECT,
        },
    ),
    put=extend_schema(
        summary="Полное обновление задачи",
        description="Полностью обновляет все данные задачи. Обязательны все поля.",
        request=TaskUpdateSerializer,
        responses={
            200: TaskUpdateSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
    ),
    patch=extend_schema(
        summary="Частичное обновление задачи",
        description="Обновляет только указанные поля задачи.",
        request=TaskUpdateSerializer,
        responses={
            200: TaskUpdateSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
    ),
    delete=extend_schema(
        summary="Удалить задачу",
        description="Удаляет задачу по ID.",
        responses={
            204: None,
            404: OpenApiTypes.OBJECT,
        },
    ),
)
class TaskRetrieveUpdateAPIView(APIView):
    serializer_class = TaskUpdateSerializer

    @method_decorator(cache_page(60 * 15, key_prefix="task_detail"))
    def get(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response(
                {"status": "error", "message": "Задача не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(task)
        return Response(
            {
                "status": "success",
                "message": "Задача успешно получена",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, id):
        return self._update(request, id, partial=False)

    def patch(self, request, id):
        return self._update(request, id, partial=True)

    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response(
                {"status": "error", "message": "Задача не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update(self, request, id, partial=False):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response(
                {"status": "error", "message": "Задача не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(task, data=request.data, partial=partial)

        if not serializer.is_valid():
            return Response(
                {"status": "error", "message": "Ошибка валидации", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "Задача успешно обновлена",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
