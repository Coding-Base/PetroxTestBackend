# exams/admin.py
from django.contrib import admin
from .models import Course, Question, TestSession

admin.site.register(Course)
admin.site.register(Question)
admin.site.register(TestSession)

