from django.shortcuts import render
from .models import Course, Objective, Requirement, RALink

def predefined_query(request):
    # Example 1: Get all courses
    courses = Course.objects.all()

    # Example 2: Get objectives for a specific course
    course_id = 1  # Replace with dynamic input
    objectives = Objective.objects.filter(id_curso=course_id)

    # Example 3: Get all RA links with high importance
    ra_links = RALink.objects.filter(importancia__gte="Alta")

    context = {
        'courses': courses,
        'objectives': objectives,
        'ra_links': ra_links,
    }
    return render(request, 'course_management/query_results.html', context)

# Create a simple view for the index page
def index(request):
    return render(request, 'course_management/index.html')
