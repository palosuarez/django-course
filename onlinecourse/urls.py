from django.urls import path
from django.views.generic import ListView, DetailView
from . import views
from .models import Course

app_name = 'onlinecourse'

urlpatterns = [
    # Lista de cursos
    path(
        '',
        ListView.as_view(
            model=Course,
            template_name='onlinecourse/course_list.html',
            context_object_name='courses'
        ),
        name='courses'
    ),
    
    # Detalles del curso (formulario de examen)
    path(
        'course/<int:pk>',
        DetailView.as_view(
            model=Course,
            template_name='onlinecourse/course_details_bootstrap.html',
            context_object_name='course'
        ),
        name='course_details'
    ),
    
    # Enviar respuestas del examen
    path(
        'course/<int:course_id>/submit',
        views.submit,
        name='submit'
    ),
    
    # Ver resultados del examen
    path(
        'submission/<int:submission_id>/result',
        views.show_exam_result,
        name='show_exam_result'
    ),
]