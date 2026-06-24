from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_word, name="inicio_buscador")
]