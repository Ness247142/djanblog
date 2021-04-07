from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse_lazy, reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default=" ")
    linkedin_url = models.CharField(max_length=200, null=True, blank=True)
    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    twitter_url = models.CharField(max_length=200, null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)
    pinterest_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('home')

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
