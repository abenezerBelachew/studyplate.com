from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from uuid import uuid4


class University(models.Model):
    """
    Contains details about a university.
    """
    id = models.UUIDField( # new
        primary_key=True,
        default=uuid4,
        editable=False,
        max_length=70)
    name = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=25, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(null=False, unique=True, max_length=200)

    class Meta:
        verbose_name_plural = "Universities"
    
    def get_absolute_url(self):
        return reverse("university:university_detail_and_courses", 
                kwargs={"uni_slug": self.slug})
    
    def save(self, *args, **kwargs):
        # slugify the name and set it as the slug of the university
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.name)


class Faculty(models.Model):
    """
    Contains details about the faculties at a 
    specific university
    """
    name = models.CharField(max_length=70)
    university = models.ForeignKey(University, on_delete=models.CASCADE,
            related_name='faculties')
    slug = models.SlugField(null=False, unique=True, max_length=200)

    class Meta:
        verbose_name_plural = "Faculties"
    
    def save(self, *args, **kwargs):
        # slugify the name and set it as the slug of the faculty
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.name)
    