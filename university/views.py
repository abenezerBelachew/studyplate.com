from django.contrib.auth.decorators import login_required
# For pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import University

def home(request):
    return render(request, 'home.html', {})

class UniversityListView(ListView):
    """ List of universities """
    model = University
    template_name = 'uni/uni_list.html'
    context_object_name = 'universities'


def university_detail_and_courses(request, uni_slug):
    university = get_object_or_404(University, slug=uni_slug)
    course_list = university.uni_courses.all() #TODO: prolly can be improved to reduce query

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(course_list, 15)

    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages) 

    context = {'university': university, 'courses': courses}    
    return render(request, 'uni/uni_detail_and_courses.html', context)