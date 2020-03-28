from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify


# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/cover_pics/user-<id>-<filename>
    # upload_to='documents/%Y/%m/%d/'
    return f'cover_pics/user-{instance.author.id}_{filename}'


class Category(models.Model):
    CATEGORY_CHOICES = [("news", "news"), ("tech", "tech"), ("fashion", "fashion"), ("politics", "politics"),
                        ("health", "health"), ("entertainment", "entertainment"),
                        ("sport", "sport")]

    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'categories'
        verbose_name = 'category'

    def __str__(self):
        return str(self.name).title()


class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to=user_directory_path, blank=True, null=True)  # default='cover_pics/default.jpg'
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', null=False)
    tags = TaggableManager()
    short_description = models.CharField(max_length=170, null=True, blank=True)
    slug = models.SlugField(unique=True, null=False, max_length=200)

    def __str__(self):
        return self.title

    # method to get the url of a specific post
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk, 'slug': self.slug})
        # url to redirect to is the name='post_detail'

        # Should've used redirect function but:
        # reverse returns a full url route as a string while redirect actually redirects you to a specific route

        # The View calling this method will get the url and handle the redirect


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    website = models.URLField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)  # to approve comment on a page from admin to prevent spamming

    class Meta:
        ordering = ['-created_on']

    # default human-readable representation of the object
    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
