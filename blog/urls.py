"""
    name='urls',
    project='ideacloud'
    date='2/28/2020',
    author='Oshodi Kolapo',
"""
from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.all_category, name='all_category'),

    path('', views.home_page, name='blog-home'),
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user_posts'),

    # re-route to a single post with the post's pk : 'post/3'
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),

    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('about/', views.about, name='blog-about'),
    path('post/tag/<str:tags>/', views.tag_posts, name='post_tags'),

    path('category/<str:categories>/', views.PostCategoryListView.as_view(), name='category')
]
