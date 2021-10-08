from django.urls import path

from .views import post_and_comments, \
                    delete_comment, \
                    delete_post, like_post


app_name="posts"


urlpatterns = [
    # path('<slug:uni_slug>/courses/<slug:course_slug>/create/', post_create, name='post_create'),
    path('<slug:uni_slug>/courses/<slug:course_slug>/post/<slug:post_slug>/', post_and_comments, name='post_and_comments'),
    # path('<slug:uni_slug>/courses/<slug:course_slug>/post/<slug:post_slug>/comment', create_comment, name='create_comment'),
    path('<slug:uni_slug>/courses/<slug:course_slug>/post/<slug:post_slug>/delete', delete_post, name='delete_post'),
    path('<slug:uni_slug>/courses/<slug:course_slug>/post/<slug:post_slug>/comments/<slug:comment_slug>/delete', delete_comment, name='delete_comment'),
    path('like/', like_post, name='like_post'),
    
]