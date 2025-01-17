from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    
    path('ask-question/', views.perguntar_produto, name='perguntar_produto'),
]