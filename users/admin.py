from django.contrib import admin
from .models import Profile
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class ProfileAdmin(ImportExportModelAdmin):
    pass
    # list_display = ('username', 'email')


class MyUserAdmin(ImportExportModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'is_superuser',)
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
