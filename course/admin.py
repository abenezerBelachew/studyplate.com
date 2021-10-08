from django.contrib import admin

from university.models import University
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    prepopulated_fields = {'slug': ('code', 'name')}