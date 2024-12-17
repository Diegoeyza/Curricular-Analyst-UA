from django.urls import path
from . import views

urlpatterns = [
    # Define URL patterns for your app here
    path('', views.index, name='index'),  # Example URL pattern
]
