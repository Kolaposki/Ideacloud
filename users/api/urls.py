from .views import *
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('register/', api_registration_view, name='api_register'),
]
