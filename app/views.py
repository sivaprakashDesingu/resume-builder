from django.shortcuts import render


def home(request):
    """Render the home page template."""
    return render(request, 'app/pages/home.html')


def about(request):
    """Render the about page template."""
    return render(request, 'app/pages/about.html')


def resume_explorer(request):
    """Render the resume explorer listing page."""
    return render(request, 'app/pages/resume_explorer.html')


def resume1(request):
    """Render the resume 1 template."""
    return render(request, 'app/resumes/resume1.html')


def resume_detail(request, pk: int):
    """Dynamically serve resume templates (e.g., resume1.html, resume2.html, resume3.html)."""
    template_name = f'app/resumes/resume{pk}.html'
    return render(request, template_name)