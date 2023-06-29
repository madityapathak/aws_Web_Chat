from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('users/', views.getAllUsers),
    path('user/<str:pk>/', views.getUser),
    path('rooms/', views.getAllRooms),
    path('room/<str:pk>/', views.getRoom),
]
