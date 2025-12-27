from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('about', views.about),  # without slash

    # Prefill form to capture user basics before building resume
    path('start/', views.start_resume, name='start_resume'),

    path('resume-eplorer/', views.resume_explorer, name='resume_explorer'),
    path('resume-eplorer', views.resume_explorer),  # without slash
    # Common alternate routes people may type (underscore, extensions, missing slash)
    path('resume_explorer', views.resume_explorer, name='resume_explorer_underscore'),
    path('resume_explorer/', views.resume_explorer),
    path('resume_explorer.html', views.resume_explorer),
    path('resume_explorer.htnl', views.resume_explorer),
    path('resume-eplorer/upload/', views.resume_upload, name='resume_upload'),
    path('resume-eplorer/<int:pk>/', views.resume_editor, name='resume_detail'),
    path('resume_explorer/<int:pk>/', views.resume_editor, name='resume_detail_underscore'),
    path('resume1/', views.resume1, name='resume1'),
    path('resume1', views.resume1),
    path('resume1.html', views.resume1),
]
