from django.urls import path
from . import views

urlpatterns = [
    path('', views.listview, name='tasks'),
    path('delete/', views.delete_task_view, name='delete_task')
]
