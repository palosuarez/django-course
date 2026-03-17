from django.db import models
from django.contrib.auth.models import User

class Instructor(models.Model):
    """Modelo de Instructor"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"Instructor: {self.user.username}"

class Learner(models.Model):
    """Modelo de Aprendiz"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Learner: {self.user.username}"

class Course(models.Model):
    """Modelo de Curso"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True)
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

class Question(models.Model):
    """Modelo de Pregunta"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.TextField(help_text="Enunciado de la pregunta")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['lesson', 'created_at']
    
    def __str__(self):
        return f"Q: {self.question_text[:50]}..."
    
    def is_get_score(self):
        """Calcula si la pregunta fue respondida correctamente"""
        correct_count = self.choice_set.filter(is_correct=True).count()
        return correct_count > 0

class Choice(models.Model):
    """Modelo de Opción"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['question', 'created_at']
    
    def __str__(self):
        status = "✓" if self.is_correct else "✗"
        return f"{status} {self.choice_text[:50]}"

class Submission(models.Model):
    """Modelo de Envío"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(Learner, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=100, blank=True)
    choices = models.ManyToManyField(Choice)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.user} - {self.course} - {self.submitted_at}"