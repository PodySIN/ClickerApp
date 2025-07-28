from django.urls import path
from . import views

urlpatterns = [
    path("", views.StandartUserListCreateAPIView.as_view(), name="all-users"),
    path("create-admin/", views.CreateAdminView.as_view(), name="create-admin"),
    path("<int:id>/", views.StandartUserRetrieveUpdateAPIView.as_view(), name="user-detail"),
]
