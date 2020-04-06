from django.db import models
from django.contrib.auth.models import User

# imports for token and authentication
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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


# for token authentication when the user creates an account. A token is generated after registering
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # if a User is created and saved to the db
        Token.objects.create(user=instance)  # generate a token for that specific user account
