from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('task/<uuid:pk>', views.task_detail, name='task_detail'),
    
    path('create/', views.create_task, name='task_create'),
]