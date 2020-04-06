from .views import *
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users'

urlpatterns = [
    path('register/', api_registration_view, name='api_register'),
    path('login/', obtain_auth_token, name='api_login'),  # returns token of the logged in user
    path('user-token/', CustomAuthToken.as_view()),  # returns token of user
]
