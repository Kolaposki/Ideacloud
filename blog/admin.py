from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin


# Register your models here.


class PostAdmin(ImportExportModelAdmin, SummernoteModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'date_posted', 'slug')
    summernote_fields = ('content',)
    search_fields = ('title', 'author',)
    prepopulated_fields = {'slug': ('title',)}  # auto add the title to the slug field
    list_display_links = ('id', 'title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    # prepopulated_fields = {'slug': ('name',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments', ]

    # This will help us for approving many comment objects at once,
    # takes a queryset and updates the active boolean field to True.
    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.unregister(Group)
