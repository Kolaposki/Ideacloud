from rest_framework import serializers
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_post_author')  # register a field using a function

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date_posted', 'cover', 'view_count', 'username', ]

    def get_post_author(self, blog_post):
        username = blog_post.author.username
        return username
