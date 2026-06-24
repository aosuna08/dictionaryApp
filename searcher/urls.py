from django.urls import path
from django import views

urlpatterns = [
    path('', views.search_word, name="inicio_buscador")
]