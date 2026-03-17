from django.contrib import admin
from django.contrib.auth.models import User
from .models import Course, Lesson, Question, Choice, Submission


# ============ INLINES ============

class ChoiceInline(admin.TabularInline):
    """Editar opciones dentro de pregunta"""
    model = Choice
    extra = 4
    fields = ('content', 'is_correct')
    ordering = ('created_at',)


class QuestionInline(admin.StackedInline):
    """Editar preguntas dentro de lección"""
    model = Question
    extra = 2
    fields = ('content', 'lesson')
    ordering = ('created_at',)


# ============ ADMINS ============

class QuestionAdmin(admin.ModelAdmin):
    """Admin para preguntas"""
    inlines = [ChoiceInline]
    list_display = ('content_preview', 'course', 'lesson', 'created_at')
    search_fields = ('content', 'course__name')
    list_filter = ('course', 'lesson', 'created_at')
    ordering = ('-created_at',)
    
    def content_preview(self, obj):
        return f"{obj.content[:80]}..."
    content_preview.short_description = "Pregunta"


class LessonAdmin(admin.ModelAdmin):
    """Admin para lecciones"""
    inlines = [QuestionInline]
    list_display = ('title', 'course', 'order', 'created_at')
    search_fields = ('title', 'course__name')
    list_filter = ('course', 'created_at')
    ordering = ('course', 'order')


class CourseAdmin(admin.ModelAdmin):
    """Admin para cursos"""
    list_display = ('name', 'question_count', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    
    def question_count(self, obj):
        return obj.question_set.count()
    question_count.short_description = "Preguntas"


class SubmissionAdmin(admin.ModelAdmin):
    """Admin para envíos"""
    list_display = ('user', 'course', 'submitted_at')
    search_fields = ('user__username', 'course__name')
    list_filter = ('course', 'submitted_at', 'user')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)


# ============ REGISTRAR EN ADMIN ============

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(User)