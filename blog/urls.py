from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', views.task_list),
    path('<int:pk>/', views.task_detail),
    path('create/', views.task_create),
]
