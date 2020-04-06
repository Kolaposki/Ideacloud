from .views import *
from django.urls import path

# from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users'

urlpatterns = [
    path('register/', api_registration_view, name='api_register'),
    path('account-update/', update_user_view, name='api_user_update'),
    path('account-detail/', user_detail_view, name='api_user_detail'),
    path('login/', ObtainAuthTokenView.as_view(), name='api_login'),  # returns token of the logged in user
    path('user-token/', CustomAuthToken.as_view()),  # returns token of user
]
