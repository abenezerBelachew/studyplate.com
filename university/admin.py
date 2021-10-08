from django.contrib import admin

# from course.models import Course
from .models import University, Faculty
# from course.models import Course


# class CourseInLine(admin.TabularInline):
#     model = Course

class FacultyInline(admin.TabularInline):
    model = Faculty

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description',)
    prepopulated_fields = {'slug': ('name', )}
    list_filter = ('name', )
    search_fields = ('name', 'description',)
    inlines = [FacultyInline]

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'university')
    prepopulated_fields = {'slug': ('name', )}