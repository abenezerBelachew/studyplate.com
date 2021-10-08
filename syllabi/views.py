from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, \
    get_object_or_404, get_list_or_404, HttpResponse
from django.contrib.auth.decorators import login_required



from university.models import University
from course.models import Course

from .models import Syllabus
from .forms import SyllabusFileForm, SyllabusLinkForm



@login_required
def syllabus_upload(request, uni_slug, course_slug):
    course = Course.objects.get(slug=course_slug)
    university = University.objects.get(slug=uni_slug)

    if request.method == 'POST':
        form = SyllabusFileForm(request.POST, request.FILES)

        if form.is_valid():
            new_syllabus = form.save(commit=False)
            new_syllabus.uploaded_by = request.user
            new_syllabus.course = course
            new_syllabus.university = university
            new_syllabus.save()


            messages.success(request, "Syllabus uploaded. Thank you!")
            return redirect('syllabi:syllabus_list', 
                    uni_slug = uni_slug,
                    course_slug=course_slug)
    
    else:
        form = SyllabusFileForm()
    
    context = {'syllabus_form': form, 'course': course, 'university': university}
    
    return render(request, 'syllabi/upload_syllabus.html', 
        context)

@login_required
def syllabus_link_upload(request, uni_slug, course_slug):
    course = Course.objects.get(slug=course_slug)
    university = University.objects.get(slug=uni_slug)

    if request.method == 'POST':
        form = SyllabusLinkForm(request.POST)
        
        if form.is_valid():
            new_syllabus = form.save(commit=False)
            new_syllabus.uploaded_by = request.user
            new_syllabus.course = course
            new_syllabus.university = university
            new_syllabus.save()


            messages.success(request, "Syllabus uploaded. Thank you!")
            return redirect('syllabi:syllabus_list', 
                    uni_slug = uni_slug,
                    course_slug=course_slug)
    
    else:
        form = SyllabusLinkForm()
    
    context = {'syllabus_link_form': form, 'course': course, 'university': university}
    
    return render(request, 'syllabi/upload_syllabus_link.html', 
        context)

def syllabus_detail(request, uni_slug, course_slug, syllabus_slug):
    syllabus = get_object_or_404(Syllabus, slug=syllabus_slug, course__slug=course_slug, university__slug=uni_slug)
    

    # liked = False
    # if post.likes.filter(id=request.user.id):
    #     liked=True
    # else:
    #     liked=False
    
    context = {'syllabus': syllabus} #, 'liked': liked, 'comments': comments}
    return render(request, 'syllabi/syllabus_detail.html', 
            context)

def syllabus_list(request, uni_slug, course_slug):
    # try:
        
    
    # except:
    #     return HttpResponse('no syllabus found. Go back')
    # TODO: don't really need the course here
    university = get_object_or_404(University, slug=uni_slug)
    course = get_object_or_404(Course, slug=course_slug)
    syllabi = Syllabus.objects.filter(course=course)

    # get_list_or_404(Syllabus, course__slug=course_slug, 
    #                         university__slug=uni_slug)
    if request.method == 'POST':
        form = SyllabusFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_syllabus = form.save(commit=False)
            new_syllabus.uploaded_by = request.user
            new_syllabus.course = course
            new_syllabus.university = university
            new_syllabus.save()

            messages.success(request, "❤ Danke!")
            return redirect('syllabi:syllabus_list', 
                    uni_slug = uni_slug,
                    course_slug=course_slug)
    
    else:
        form = SyllabusFileForm()
        
    
    context = {'syllabi': syllabi, 'course': course, 
                'syllabus_form': form}
    
    return render(request, 'syllabi/syllabi_list.html', 
        context)



@login_required
def syllabus_delete(request, uni_slug, course_slug, syllabus_slug):
    # change id to UUID or sth more secure. It sucks right now
    syllabus = get_object_or_404(Syllabus, slug=syllabus_slug, uploaded_by=request.user)
    
    if request.method == 'POST':
        syllabus.delete()

        messages.success(request, 'Syllabus deleted!')
        return redirect('syllabi:syllabus_list', 
                    uni_slug=uni_slug, 
                    course_slug=course_slug)

    # TODO: why is this not working?
    # else:
    #     # If the user is not the author of the post, send them this message
    #     raise PermissionDenied
    
    return render(request, 'syllabi/delete_syllabus.html', {'syllabus': syllabus})
