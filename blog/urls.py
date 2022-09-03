from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('login/', views.login),
    path('user/', views.get_user_details),
    path('register/', views.register),
    path('', views.list_blog),
    path('<int:pk>/', views.blog_details),
    path('create/', views.create_blog),
]
