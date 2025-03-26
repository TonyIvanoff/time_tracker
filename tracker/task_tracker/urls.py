from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('task/<str:task_id>', views.task_detail, name='task_detail'),
    # path('task/create/', views.task_create, name='task_create'),
]