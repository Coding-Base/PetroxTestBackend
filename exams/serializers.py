# exams/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, Question, TestSession

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
class TestSessionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    duration = serializers.IntegerField()

    class Meta:
        model = TestSession
        fields = ['id', 'user', 'course', 'questions', 'start_time', 'end_time', 'score', 'duration']
