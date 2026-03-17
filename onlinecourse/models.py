from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    """Modelo de Curso"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Modelo de Lección"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.name} - {self.title}"


# ============ NUEVOS MODELOS ============

class Question(models.Model):
    """Modelo de Pregunta"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    content = models.TextField(
        help_text="Enunciado de la pregunta"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['lesson', 'created_at']
    
    def __str__(self):
        return f"Q: {self.content[:50]}..."


class Choice(models.Model):
    """Modelo de Opción de respuesta"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(
        max_length=1000,
        help_text="Texto de la opción"
    )
    is_correct = models.BooleanField(
        default=False,
        help_text="¿Es esta la respuesta correcta?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['question', 'created_at']
    
    def __str__(self):
        status = "✓" if self.is_correct else "✗"
        return f"{status} {self.content[:50]}"


class Submission(models.Model):
    """Modelo de Envío/Intento de examen"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choices = models.ManyToManyField(
        Choice,
        help_text="Opciones seleccionadas por el usuario"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.name} - {self.submitted_at}"