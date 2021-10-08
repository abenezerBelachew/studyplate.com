from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from uuid import uuid4

# Create your models here.
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=75, blank=True)
    # email = models.EmailField(unique=True, help_text='Your ualberta email', max_length=150)
    bio = models.TextField(max_length=100, blank=True, 
        help_text="Something you want to share.")
    # For the avatar
    identifier = models.CharField(max_length=30, default=str(uuid4())[:4])
    
    def get_absolute_url(self):
        return reverse("account:user_detail", kwargs={"username": self.username, })
    
    def joined_courses(self):
        return self.course_followers.select_related('university').all()

    def __str__(self):
        return str(self.full_name)

    
    

