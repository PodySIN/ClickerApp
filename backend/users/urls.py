from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserListCreateAPIView.as_view(), name="all-users"),
    path("<int:id>/", views.UserRetrieveUpdateAPIView.as_view(), name="user-detail"),
]
