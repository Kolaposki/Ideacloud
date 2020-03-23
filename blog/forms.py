"""
    name='forms',
    project='ideabank'
    date='3/13/2020',
    author='Oshodi Kolapo',
"""

from .models import Comment, Post
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class PostForm(forms.ModelForm):
    # CATEGORY_CHOICES = [(1, "news"), (2, "tech"), (3, "fashion"), (4, "politics"), (5, "health"), (6, "entertainment"),
    #                   (7, "sport")]

    CATEGORY_CHOICES = [("news", "news"), ("tech", "tech"), ("fashion", "fashion"), ("politics", "politics"),
                        ("health", "health"), ("entertainment", "entertainment"),
                        ("sport", "sport")]

    content = forms.CharField(widget=SummernoteWidget())  # instead of forms.Textarea
    title = forms.CharField(max_length=120, required=True, strip=True)
    cover = forms.ImageField(required=False)

    #s category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True, label="Category")

    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'cover', 'tags')


class CommentForm(forms.ModelForm):
    email = forms.EmailField()
    website = forms.URLField(initial='http://', required=False)

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'website')
