from django.urls import path
from .views import registration, login

urlpatterns = [
    path('register/', registration, name='register'),
    path('login/', login, name='login')
]