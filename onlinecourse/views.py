from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Course, Submission, Choice


@login_required(login_url='/admin/login/')
def submit(request, course_id):
    """
    Procesar envío de respuestas del examen
    
    POST: Crear submission con choices seleccionadas
    Redirigir a resultado
    """
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        # Crear nuevo submission
        submission = Submission.objects.create(
            course=course,
            user=request.user
        )
        
        # Obtener choices seleccionados (checkboxes)
        choice_ids = request.POST.getlist('choices')
        if choice_ids:
            choices = Choice.objects.filter(id__in=choice_ids)
            submission.choices.set(choices)
        
        # Redirigir a resultados
        return redirect('onlinecourse:show_exam_result', submission_id=submission.id)

    
    return redirect('onlinecourse:course_details', pk=course_id)


@login_required(login_url='/admin/login/')
def show_exam_result(request, submission_id):
    """
    Mostrar resultados del examen con calificación
    
    Calcula score basado en respuestas correctas
    Muestra detalles de cada pregunta
    """
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Seguridad: solo el dueño puede ver su resultado
    if submission.user != request.user:
        raise Http404("No tienes permiso para ver este resultado")
    
    course = submission.course
    
    # ============ LÓGICA DE CALIFICACIÓN ============
    correct_count = 0
    total_questions = course.question_set.count()
    
    for question in course.question_set.all():
        # Obtener respuestas correctas de la pregunta
        correct_choices = set(question.choice_set.filter(is_correct=True))
        
        # Obtener respuestas seleccionadas por el usuario
        user_choices = set(submission.choices.filter(question=question))
        
        # Si coinciden exactamente, es correcta
        if correct_choices == user_choices and user_choices:
            correct_count += 1
    
    # Calcular score
    if total_questions > 0:
        score = int((correct_count / total_questions) * 100)
    else:
        score = 0
    
    # Determinar aprobado/fallido (punto de corte: 60%)
    passed = score >= 60
    
    # ============ CONTEXTO PARA TEMPLATE ============
    context = {
        'course': course,
        'submission': submission,
        'correct_count': correct_count,
        'total_questions': total_questions,
        'score': score,
        'passed': passed,
        'choices': submission.choices.all(),
    }
    
    return render(request, 'onlinecourse/exam_result.html', context)
