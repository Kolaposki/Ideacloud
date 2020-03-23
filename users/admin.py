from django.contrib import admin
from .models import Profile


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    pass
    # list_display = ('username', 'email')


admin.site.register(Profile, ProfileAdmin)
