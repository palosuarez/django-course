from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission, Instructor, Learner

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    fields = ('choice_text', 'is_correct')

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 2

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'instructor', 'created_at')
    search_fields = ('name',)

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'course', 'order')

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'course', 'lesson')
    search_fields = ('question_text',)

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

class LearnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrollment_date')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'submitted_at')

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)