from django.urls import path
from . import views

app_name = 'cieloAdmin'

urlpatterns = [
    path('', views.index, name='index'),
]
