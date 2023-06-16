from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # # additional field
    # portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    # this file will be send to media/profiles_pics

    def __str__(self):
        return self.user.username
    
class TemplateFile(models.Model):
    name = models.CharField(max_length=500)
    filepath = models.FileField(upload_to='files/templates', null=True)

    def __str__(self):
        return self.name
    
class File(models.Model):
    name = models.CharField(max_length=500)
    filepath = models.FileField(upload_to='files/', null=True)

    def __str__(self):
        return self.name
