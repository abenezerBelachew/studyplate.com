from django.urls import path

from .views import home, UniversityListView, university_detail_and_courses

app_name = 'university'

urlpatterns = [
    path('universities/', UniversityListView.as_view(), name='uni_list'),
    path('<slug:uni_slug>/', university_detail_and_courses, 
        name='university_detail_and_courses'),
]