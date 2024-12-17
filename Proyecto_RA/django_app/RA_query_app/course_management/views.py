from django.shortcuts import render
from django.db.models import Q
from django.db import connection  # To execute raw SQL queries
from .models import Course, Objective, Requirement, RALink

# View for the home menu
def index(request):
    return render(request, 'course_management/index.html')

# View to handle predefined queries
def predefined_query(request):
    query_type = request.GET.get('query_type')  # Determines which query to execute
    user_input = request.GET.get('user_input')  # User input for the query
    results = None
    query_description = ""

    if query_type == "all_courses":
        results = Course.objects.values("id_curso", "nombre")  # Fetch id_curso and nombre
        query_description = "All Courses"

    elif query_type == "objectives_for_course":
        if user_input:
            # Perform a case-insensitive search for both `id_curso` and `nombre`
            results = Objective.objects.filter(
                Q(id_curso__iexact=user_input) | Q(nombre__icontains=user_input)
            ).values("nombre", "objetivo", "id_curso")
            query_description = f"Objectives for Course (ID or Name): {user_input}"
        else:
            query_description = "Please provide a valid Course ID or Name."

    elif query_type == "ra_links_high_importance":
        results = RALink.objects.filter(importancia__icontains="Alta")
        query_description = "RA Links with High Importance"

    elif query_type == "requirements_for_course":
        if user_input:
            results = Requirement.objects.filter(id_curso=user_input).values("id_curso","id_requisito")
            query_description = f"Requirements for Course ID {user_input}"
        else:
            query_description = "Please provide a valid Course ID."

    elif query_type == "objetivos_terminales":
        # Raw SQL query to get terminal objectives
        query = """
        SELECT 
            o.id_objetivo,
            o.nombre as curso,
            o.objetivo
        FROM 
            course_management_objective o
        JOIN 
            course_management_ralink rl ON o.id_objetivo = rl.id_objetivo_prerequisito
        WHERE 
            NOT EXISTS (
                SELECT 1
                FROM course_management_ralink rl2
                WHERE rl2.id_objetivo_prerequisito = o.id_objetivo
                AND rl2.id_objetivo != rl.id_objetivo
            )
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        query_description = "Terminal Objectives (Objetivos Terminales)"

    context = {
        'results': results,
        'query_description': query_description,
        'query_type': query_type,
        'user_input': user_input,
    }
    return render(request, 'course_management/query_results.html', context)
