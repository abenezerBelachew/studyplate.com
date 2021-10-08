from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model

from .forms import CustomUserChangeForm
from uuid import uuid4

User = get_user_model()


@login_required
def user_dashboard(request):
    user = request.user

    user_courses = user.course_followers.select_related('university').all() 

    context = {'user': user, 'user_courses': user_courses}
    return render(request, 'account/dashboard.html', context)


@login_required
def user_detail(request, username):
    """
    Get a specific users detail. To be used for profile page.
    """
    user = get_object_or_404(User,
                            username=username,
                            is_active=True)
    # To Edit Profile
    if request.method == 'POST':
        user_form = CustomUserChangeForm(instance=request.user,
                                    data=request.POST)
        # profile_form = ProfileChangeForm(instance=request.user.profile,
        #                         data = request.POST,
        #                         files = request.FILES)
        
        if user_form.is_valid(): # and profile_form.is_valid():
            user_form.save()
            # profile_form.save()
            messages.success(request, 'Profile updated successfully')
            
        
            return redirect('account:user_detail', 
                    username = request.user.username)

        else:
            messages.error(request, 'Error updating your profile')
    
    else:
        user_form = CustomUserChangeForm(instance = request.user)
        # profile_form = ProfileChangeForm(instance=request.user.profile)
        
    
    posts = user.post_author.select_related('course').all()

    context = {'user': user,
     'user_form': user_form}
    #  'profile_form': profile_form}
    
    return render(request,
                'account/user_detail.html',
                context) #, 'posts': posts})

@login_required
def user_posts(request, username):
    """
    Get the posts for a specific user.
    """
    user = get_object_or_404(User,
                        username=username,
                        is_active=True)
    visible_posts = user.post_author.filter(anonymous=False).select_related('course').all()
    anonymous_posts = user.post_author.filter(anonymous=True).select_related('course').all()


    # Pagination
    visible_posts_page = request.GET.get('page', 1)
    visible_posts_paginator = Paginator(visible_posts, 15)

    anonymous_posts_page = request.GET.get('page', 1)
    anonymous_posts_paginator = Paginator(anonymous_posts, 15)

    try:
        visible_posts = visible_posts_paginator.page(visible_posts_page)
    except PageNotAnInteger:
        visible_posts = visible_posts_paginator.page(1)
    except EmptyPage:
        visible_posts = visible_posts_paginator.page(visible_posts_paginator.num_pages)


    try:
        anonymous_posts = anonymous_posts_paginator.page(anonymous_posts_page)
    except PageNotAnInteger:
        anonymous_posts = anonymous_posts_paginator.page(1)
    except EmptyPage:
        anonymous_posts = anonymous_posts_paginator.page(anonymous_posts_paginator.num_pages)




    return render(request,
                'account/user_posts.html',
                {'user': user, 'visible_posts': visible_posts,
                'anonymous_posts': anonymous_posts,
                })


@login_required
def change_avatar(request):
    
    user = request.user
    user.identifier = str(uuid4())[:10]
    user.save()

    return redirect(user.get_absolute_url())

