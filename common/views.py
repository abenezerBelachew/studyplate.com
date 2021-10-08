from django.shortcuts import render, redirect

def home(request):
    """
    Home Page
    """
    if request.user.is_authenticated:
        return redirect('account:user_dashboard')
    context = {}
    return render(request, 'home.html', context)