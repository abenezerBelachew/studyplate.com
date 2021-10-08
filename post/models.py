from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse


from university.models import University
from course.models import Course

from uuid import uuid4

User = get_user_model()


class Post(models.Model):
    """
    This is the model for the posts made under the d/t courses
    """
    subject = models.CharField(max_length=70)
    content = models.TextField(max_length=250, help_text="250 Characters")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
        related_name='course_posts')
    university = models.ForeignKey(University, on_delete=models.CASCADE,
        related_name='uni_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='post_author')
    anonymous = models.BooleanField(default=True, max_length=10, 
        help_text='If anonymous is checked, your name will be hidden.')
    likes = models.ManyToManyField(User, related_name='post_likes',
        blank=True)
    slug = models.SlugField(null=False, unique=True, max_length=300)


    def get_absolute_url(self):
        return reverse("posts:post_and_comments", kwargs={"post_slug": self.slug,
                                            "course_slug": self.course.slug, 
                                            "uni_slug": self.course.university.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.subject) +"-"+ str(uuid4())[:7]
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.subject)



class Comment(models.Model):
    """
    Comment to the post.
    """
    content = models.TextField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
            related_name='post_comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name='comment_author')
    slug = models.SlugField(null=False, unique=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField(default=True, max_length=10, 
        help_text='If anonymous is checked, your name will be hidden.')


    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(str(self.content)[:10]) +"-"+ str(uuid4())[:4]
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.content)[:15]