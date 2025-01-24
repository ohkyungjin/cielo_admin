from django.urls import path
from .views.views import index
from .views.auth import login

app_name = 'cieloAdmin'

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
]