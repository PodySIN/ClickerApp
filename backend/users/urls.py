from django.urls import path
from . import views

urlpatterns = [
    path("", views.UsersAPIView.as_view(), name='all-users'),
    path('<int:id>/', views.UsersAPIView.as_view(), name='user-detail')
]
