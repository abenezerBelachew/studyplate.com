from django.urls import path

from .views import user_dashboard, user_detail, user_posts, change_avatar


app_name = 'account'

urlpatterns = [
    path('', user_dashboard, name='user_dashboard'),
    path('users/@<username>/', user_detail, name='user_detail'),
    path('users/@<username>/posts', user_posts, name='user_posts'),
    path('changeavatar/', change_avatar, name='change_avatar'),
]