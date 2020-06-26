from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('delete/<name>/', views.delete, name='delete'),
]
