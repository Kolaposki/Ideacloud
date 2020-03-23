from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # a user should have a single unique pict and viceversa
    # CASCADE:delete the profile of a user if the user gets deleted but do not delete the user if the profile is deleted
    bio = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    # url_height = models.PositiveIntegerField()
    # url_width = models.PositiveIntegerField()

    image = models.ImageField(default='avatar.png', upload_to='profile_pics')

    # default image name for every new user {avatar}
    # upload the image to a folder called {profile_pics}
    # resize the image to height and width of 125px

    def __str__(self):
        return f"{self.user.username}'s profile"
