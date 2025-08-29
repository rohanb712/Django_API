from django.urls import path
from . import views

urlpatterns = [
    path('', views.action_list, name='action-list'),
    path('<int:pk>/', views.action_detail, name='action-detail'),
]