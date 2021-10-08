from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse

from uuid import uuid4
from university.models import University
from course.models import Course
from django.core.validators import FileExtensionValidator

from .validators import validate_file_extension, file_size


User = get_user_model()


from django.core.exceptions import ValidationError


def syllabus_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/course_<name>/<filename>
    return f"syllabi/{instance.university.name}/{instance.course.code}/{filename}"


class Syllabus(models.Model):
    """
    Syllabus for the different courses.
    professor, term, year
    """
    title = models.CharField(max_length=75, 
        help_text='Please provide the term, year and Professor')
    file = models.FileField(upload_to=syllabus_directory_path, 
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), file_size],
        max_length=300, help_text="Please keep the size of file below 2MiB")
    course = models.ForeignKey(Course, related_name='syllabus_course', 
        on_delete=models.CASCADE)
    university = models.ForeignKey(University, related_name='syllabus_university', 
            on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,
                related_name='syllabus_uploader')
    professor = models.CharField(max_length=75, blank=True, help_text='Name of professor')
    term = models.CharField(max_length=75, blank=True, help_text="eg. Fall")
    year = models.IntegerField(blank=True, null=True, help_text="eg. 2020")
    anonymous = models.BooleanField(default=True, max_length=10, 
        help_text='If anonymous is checked, your name will be hidden.')
    link = models.URLField(max_length=250, 
        help_text='Please provide the link to the syllabus')
    likes = models.ManyToManyField(User, 
                                related_name='syllabus_likes',
                                blank=True, default=0)
    slug = models.SlugField(null=False, unique=True, max_length=300)
    

    def get_absolute_url(self):
        return reverse("syllabi:syllabus_detail", kwargs={"syllabus_slug": self.slug,
                                        "course_slug": self.course.slug, 
                                        "uni_slug": self.university.slug})
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.professor) +"-"+ str(self.term) + str(self.year) + "-" + str(uuid4())[:9]
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.professor} | {self.term}{self.year}"

