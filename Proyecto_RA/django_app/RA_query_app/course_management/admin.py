from django.contrib import admin
from .models import Course, Objective, Requirement, RALink

admin.site.register(Course)
admin.site.register(Objective)
admin.site.register(Requirement)
admin.site.register(RALink)
