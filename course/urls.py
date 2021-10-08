from django.urls import path

from .views import course_detail_and_posts, search_course,\
    follow_course

app_name = 'course'

urlpatterns = [
    path('<slug:uni_slug>/courses/<slug:course_slug>', course_detail_and_posts, 
        name='course_detail_and_posts'),
    path('<slug:uni_slug>/search/', search_course, 
        name='search_results'),
    path('<slug:uni_slug>/courses/<slug:course_slug>/follow', follow_course, 
        name='course_follow'),
]