from rest_framework import serializers
from blog.models import Post

MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50


class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_post_author')  # register a field using a function

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date_posted', 'cover', 'category', 'username', 'slug', ]

    def get_post_author(self, blog_post):
        username = blog_post.author.username
        return username


class BlogPostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'cover']

    def validate(self, blog_post):
        try:
            title = blog_post['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            content = blog_post['content']
            if len(content) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a content longer than " + str(MIN_BODY_LENGTH) + " characters."})

        except KeyError:
            pass
        return blog_post


class BlogPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'cover', 'category', 'author']

    def save(self):
        try:
            title = self.validated_data['title']
            cover = self.validated_data['cover']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            content = self.validated_data['content']
            if len(content) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a content longer than " + str(MIN_BODY_LENGTH) + " characters."})

            category = self.validated_data['category']
            if isinstance(category, str):
                raise serializers.ValidationError(
                    {"response": "Category must be an integer from range 1-6"})

            blog_post = Post(
                author=self.validated_data['author'],
                title=title,
                content=content,
                cover=cover,
                category=category
            )

        except KeyError:
            raise serializers.ValidationError(
                {"response": "You must fill in the title, content, cover picture and category"})

        blog_post.save()
        return blog_post
