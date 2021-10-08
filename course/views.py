from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector

# For pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, redirect, get_object_or_404

from .models import Course
from university.models import University

from .forms import CourseSearchForm
from post.forms import PostForm


def course_detail_and_posts(request, uni_slug, course_slug):
    course = get_object_or_404(Course, university__slug=uni_slug, slug=course_slug)
    post_list = course.course_posts.select_related('author').all().order_by('-created_at')

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 15)

    university = University.objects.get(slug=uni_slug)

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.course = course
            new_post.university = university
            new_post.save()

            messages.success(request, 'Posted!')
            return redirect('course:course_detail_and_posts', uni_slug=uni_slug, 
                    course_slug=course_slug)
    else:
        post_form = PostForm()


    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 
    

    context= {'course': course, 'posts': posts, 'post_form': post_form}
    return render(request, 'course/course_detail_and_posts.html', context)



@login_required
def follow_course(request, uni_slug, course_slug):
    course = get_object_or_404(Course, university__slug=uni_slug, slug=course_slug)
    user = request.user

    if course.followers.filter(id=user.id).exists(): 
        course.followers.remove(user)
    else:
        course.followers.add(user)

    return redirect(course.get_absolute_url())


def search_course(request, uni_slug):
    form = CourseSearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = CourseSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # results =Course.objects.filter(code__search=query)
            results = Course.objects.annotate(
                search=SearchVector('code', 'name'),
            ).filter(search=query)

            page = request.GET.get('page', 1)
            paginator = Paginator(results, 10)

            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
                

    context = {'form': form, 'query': query, 'results': results}
    return render(request, 'course/search_course.html', context)
