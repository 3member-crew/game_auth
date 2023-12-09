from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('register/', registerAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/<username>',UserAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/<username>/update/', UserUpdateAPIView.as_view()),
    path('users/', UserListAPIView.as_view())
]