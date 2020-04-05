"""
    name='forms',
    project='ideacloud'
    date='3/13/2020',
    author='Oshodi Kolapo',
"""

from .models import Comment, Post
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class PostForm(forms.ModelForm):
    CATEGORY_CHOICES = [("news", "news"), ("tech", "tech"), ("fashion", "fashion"), ("politics", "politics"),
                        ("health", "health"), ("entertainment", "entertainment"),
                        ("sport", "sport")]

    content = forms.CharField(widget=SummernoteWidget())  # instead of forms.Textarea
    title = forms.CharField(max_length=115, required=True, strip=True, min_length=5)
    cover = forms.ImageField(required=False)
    tags = forms.CharField(required=False)
    short_description = forms.CharField(max_length=170, required=False, strip=True,
                                        help_text='Provide an optional short description')

    class Meta:
        model = Post
        fields = ('title', 'category', 'short_description', 'content', 'cover', 'tags')


class CommentForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    website = forms.URLField(initial='http://', required=False)

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'website')
