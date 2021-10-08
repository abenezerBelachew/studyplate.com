from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse

from uuid import uuid4

from university.models import University



User = get_user_model()

class Course(models.Model):
    """
    Contains detail about a course
    """
    id = models.UUIDField( # new
        primary_key=True,
        default=uuid4,
        editable=False,
        max_length=70)
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    slug = models.SlugField(null=False, blank=False, unique=True, max_length=200)
    university = models.ForeignKey(University, related_name='uni_courses',
            on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, 
            related_name='course_followers',
            blank=True)
    
    def get_absolute_url(self):
        return reverse('course:course_detail_and_posts',
                kwargs={'course_slug': self.slug, 'uni_slug': self.university.slug})
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.code) + "-" +str(uuid4())[:3]
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.name)