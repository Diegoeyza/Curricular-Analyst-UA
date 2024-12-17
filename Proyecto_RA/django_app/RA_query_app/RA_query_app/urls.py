"""
URL configuration for RA_query_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

# Import the view for the home page
from course_management import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('course_management/', include('course_management.urls')),
    path('', views.index, name='home'),  # Add this line for the root URL
    path('query_results/', views.predefined_query, name='predefined_query'),  # Predefined query results

]
