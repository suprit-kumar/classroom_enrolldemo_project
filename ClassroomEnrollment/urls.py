"""ClassroomEnrollment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from classroom_app import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.loginHtml, name='loginHtml'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('login_operation/', views.login_operation, name='login_operation'),
    path('logout/', views.logout, name='logout'),
    path('register_new_user/', views.register_new_user, name='register_new_user'),
    path('save_class_details/', views.save_class_details, name='save_class_details'),
    path('fetch_class_details/', views.fetch_class_details, name='fetch_class_details'),
    path('fetch_all_class_details/', views.fetch_all_class_details, name='fetch_all_class_details'),
    path('enroll_class/', views.enroll_class, name='enroll_class'),
    path('fetch_my_enrolled_classes/', views.fetch_my_enrolled_classes, name='fetch_my_enrolled_classes'),
]
