from .views import *
from django.urls import path

app_name = 'blog'
# url : ideacloud/api/

urlpatterns = [
    path('<slug>/', api_detail_blog_view, name='api_detail'),
    path('blog/list-blog/', ApiBlogListView.as_view(), name='api_list_detail'),
    path('update/<slug>', api_update_blog_view, name='api_update'),
    path('delete/<slug>', api_delete_blog_view, name='api_delete'),
    path('blog/create/', api_create_blog_view, name='api_create'),
    path('blog/is-author/<slug>/', api_is_author_of_post, name='api_is-author'),
]
