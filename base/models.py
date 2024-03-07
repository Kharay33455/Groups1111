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
    is_verified = models.BooleanField(default = False)
    bank_verified = models.BooleanField(default = False)
    cus_care = models.CharField(max_length = 30)


    
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
    full_picture = models.ImageField(upload_to=user_media_path, null=True, blank=True)

    def __str__(self):
        return f'{self.agent.first_name} Verification'

class Message(models.Model):
    """Collect and store user messages"""
    agent = models.ForeignKey(Agent, on_delete = models.CASCADE)
    title = models.CharField(max_length = 20, null = True, blank = True)
    message = models.CharField(max_length = 1000, null = True, blank = True)
    time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
    
class Reply(models.Model):
    """Reply Messages"""
    message = models.OneToOneField(Message, on_delete = models.CASCADE)
    body = models.CharField(max_length = 1000)
    read = models.BooleanField(default = False)

    def __str__(self):
        return f'Reply to {self.message}'


class Prompt(models.Model):
    """Store prompt for users"""
    agent = models.ForeignKey(Agent, on_delete = models.CASCADE)
    main = models.CharField(max_length = 500, null = True, blank = True)
    prompt1 = models.CharField(max_length = 100, null = True, blank = True)
    prompt2 = models.CharField(max_length = 100, null = True, blank = True)
    prompt3 = models.CharField(max_length = 100, null = True, blank = True)
    prompt4 = models.CharField(max_length = 100, null = True, blank = True)

    def __str__(self):
        return f'{self.agent.first_name} {self.agent.last_name}'
    
class BankName(models.Model):
    bank_code = models.CharField(max_length = 8, unique =True)
    bank_name = models.CharField(max_length = 30, unique = True)

    def __str__(self):
        return self.bank_name
    
class BankAccount(models.Model):
    agent = models.ForeignKey(Agent, on_delete = models.CASCADE)
    bank_name = models.ForeignKey(BankName, on_delete = models.CASCADE)
    account_number = models.CharField(max_length = 11)
    account_name = models.CharField(max_length = 50)
    account_type = models.CharField(max_length = 20)

    def __str__(self):
        return f'{self.agent.first_name} {self.agent.last_name} {self.bank_name} account.'
    
