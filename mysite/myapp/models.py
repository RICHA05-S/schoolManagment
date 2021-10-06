from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number= models.CharField(max_length=11,default='', null=True, blank= True)
    USER_TYPE_CHOICES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10,choices=USER_TYPE_CHOICES , default='Student')

    def __str__(self):
        return f'{self.user.username}'

class Subject(models.Model):
    sub_name=models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return f'{self.sub_name}'


class Marks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE) # save obj , pk
    total_marks=models.CharField(max_length=3,blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.user.username



class Resetpassword(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    token = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.user.username