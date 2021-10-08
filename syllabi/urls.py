from django.urls import path

from .views import syllabus_upload, syllabus_detail, \
    syllabus_list, syllabus_link_upload, syllabus_delete

app_name = 'syllabi'

urlpatterns = [

    path('<slug:uni_slug>/courses/<slug:course_slug>/upload/', syllabus_upload, name='syllabus_upload'),
    path('<slug:uni_slug>/courses/<slug:course_slug>/upload_link/', syllabus_link_upload, name='syllabus_upload_link'),
    path('<slug:uni_slug>/courses/<slug:course_slug>/syllabus/<slug:syllabus_slug>/', syllabus_detail, name='syllabus_detail'),
    path('<slug:uni_slug>/courses/<slug:course_slug>/syllabus/<slug:syllabus_slug>/delete/', syllabus_delete, name='syllabus_delete'),
    path('<slug:uni_slug>/courses/<slug:course_slug>/syllabi/', syllabus_list, name='syllabus_list'),

]