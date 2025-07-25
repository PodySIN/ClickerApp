from django.urls import path
from . import views

urlpatterns = [
    path("", views.LevelListCreateAPIView.as_view(), name="all-levels"),
    path("<int:level>/", views.LevelRetrieveUpdateAPIView.as_view(), name="level-detail"),
]
