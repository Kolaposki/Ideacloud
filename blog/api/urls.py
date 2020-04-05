from .views import *
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('<slug>/', api_detail_blog_view, name='api_detail'),
    path('update/<slug>', api_update_blog_view, name='api_update'),
    path('delete/<slug>', api_delete_blog_view, name='api_delete'),
    path('create/', api_create_blog_view, name='api_create'),
]
