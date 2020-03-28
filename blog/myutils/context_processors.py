from blog.models import Post, Category


def recent_posts_context(request):
    recent_posts = Post.objects.all().order_by('-date_posted')[0:4]
    return {
        'recent_posts': recent_posts
    }


def common_tags_context(request):
    common_tags = Post.tags.most_common()[0:8]
    return {'common_tags': common_tags}
