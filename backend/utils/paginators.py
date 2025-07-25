from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, status, message, data, status_code):
        return Response(
            {
                "status": status,
                "message": message,
                "support_data": {
                    "links": {"next": self.get_next_link(), "previous": self.get_previous_link()},
                    "count": self.page.paginator.count,
                    "page_size": self.get_page_size(self.request),
                },
                "data": data,
            },
            status=status_code,
        )
