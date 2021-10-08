from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render, get_object_or_404


from .models import Post, Comment
from university.models import University
from course.models import Course
from .forms import PostForm, CommentForm
from common.decorators import ajax_required


def post_and_comments(request, uni_slug, course_slug, post_slug):
    post = get_object_or_404(Post, slug=post_slug, course__slug=course_slug, university__slug=uni_slug)
    comments = post.post_comment.select_related('author').all()

    liked = False
    if post.likes.filter(id=request.user.id):
        liked=True
    else:
        liked=False
    
    # So users can comment from the same page instead of going to another page
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post

            new_comment.save()

            # messages.success(request, 'Posted!')

            return redirect('posts:post_and_comments', 
                    post_slug=post_slug,
                    uni_slug=uni_slug, 
                    course_slug=course_slug)
    
    else:
        comment_form = CommentForm()

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 15)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context = {'post': post, 'liked': liked, 'comments': comments,
                'comment_form': comment_form}
    return render(request, 'posts/post_and_comments.html', 
            context)












@login_required
def delete_post(request, post_slug, uni_slug, course_slug):
    # change id to UUID or sth more secure. It sucks right now
    post = get_object_or_404(Post, slug=post_slug, author=request.user)
    
    if (request.method == 'POST') and (request.user == post.author):
        post.delete()

        messages.success(request, 'Your post has been deleted!')
        return redirect('course:course_detail_and_posts', 
                    uni_slug=uni_slug, 
                    course_slug=course_slug)

    # TODO: why is this not working?
    # else:
    #     # If the user is not the author of the post, send them this message
    #     raise PermissionDenied
    
    return render(request, 'posts/delete_post.html', {'post': post})





@login_required
def delete_comment(request, comment_slug, post_slug, uni_slug, course_slug):
    # TODO: change id to UUID or sth more secure. It sucks right now
    comment = get_object_or_404(Comment, slug=comment_slug, author=request.user)
    
    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
        
        messages.success(request, 'Reply deleted successfully.')
        
        return redirect('posts:post_and_comments',
                    post_slug=post_slug, uni_slug=uni_slug, 
                    course_slug=course_slug)
    # else:
    #     return HttpResponse("<a href='https://www.youtube.com/watch?v=dI0XWAMQgxc'>I don't think \
    #         you have the facilities, big man.")

    
    return render(request, 'posts/delete_comment.html', {'comment': comment})




@login_required
@ajax_required
@require_POST    # returns STATUS CODE 405 if request not done via post
def like_post(request):
    user = request.user
    post_slug = request.POST.get('slug')
    action = request.POST.get('action')

    if post_slug and action:
        try:
            post = Post.objects.get(slug=post_slug)
            
            if action == 'like':
                post.likes.add(user)
            else:
                post.likes.remove(user)
            return JsonResponse({'status': 'ok'})
        
        except:
            pass

    return JsonResponse({'status': 'error'})