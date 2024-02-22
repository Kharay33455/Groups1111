from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    date_of_birth = models.DateField()
    phone_number = models.IntegerField()

    
    def __str__(self):
        return f'{self.first_name + " "+self.last_name}'
    

class Address(models.Model):
    house_number = models.IntegerField()
    street = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

def user_media_path(instance, filename):
    # Generate the upload path based on the user's username
    username = instance.user.username
    upload_to = os.path.join('uploads', 'user_{0}'.format(username), filename)
    return upload_to

class Verification(models.Model):
    """To veryfy users to use premium services"""
    agent = models.OneToOneField(Agent, on_delete = models.CASCADE)
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    nin_front = models.ImageField(upload_to=user_media_path, null = True, blank= True)
    nin_back = models.ImageField(upload_to=user_media_path, null = True, blank= True)
    proclaim_video = models.FileField(upload_to= user_media_path, null = True, blank = True)