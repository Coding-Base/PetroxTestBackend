# exams/views.py
import random
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth.models import User
from .models import Course, Question, TestSession
from .serializers import CourseSerializer, QuestionSerializer, TestSessionSerializer

# Endpoint to list courses
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

# Admin endpoint to add a question
class AddQuestionAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Endpoint to start a test (select N random questions from a course)
class StartTestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        course_id = request.data.get('course_id')
        question_count = int(request.data.get('question_count', 0))
        duration = request.data.get('duration')  # ✅ Retrieve duration as is
        
        if duration is None or not str(duration).isdigit():
            return Response({"error": "Invalid duration provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        duration = int(duration)  # ✅ Convert to integer after validation

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
        all_questions = list(Question.objects.filter(course=course))
        if question_count > len(all_questions):
            return Response({"error": "Not enough questions in the course"}, status=status.HTTP_400_BAD_REQUEST)
        
        selected_questions = random.sample(all_questions, question_count)

        test_session = TestSession.objects.create(
            user=request.user,
            course=course,
            duration=duration  # ✅ Save the user-specified duration
        )
        test_session.questions.set(selected_questions)
        test_session.save()
        
        serializer = TestSessionSerializer(test_session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Endpoint to submit a test
class SubmitTestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, session_id):
        try:
            test_session = TestSession.objects.get(id=session_id, user=request.user)
        except TestSession.DoesNotExist:
            return Response({"error": "Test session not found"}, status=status.HTTP_404_NOT_FOUND)
        
        answers = request.data.get('answers', {})
        score = 0
        for question in test_session.questions.all():
            user_answer = answers.get(str(question.id))
            if user_answer and user_answer.upper() == question.correct_option.upper():
                score += 1
        
        test_session.score = score
        test_session.end_time = timezone.now()  # Ensure timezone-aware datetime
        test_session.save()
        
        serializer = TestSessionSerializer(test_session)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Endpoint to list test history for the logged-in user
class TestHistoryAPIView(generics.ListAPIView):
    serializer_class = TestSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TestSession.objects.filter(user=self.request.user).order_by('-start_time')

class RegisterUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow anyone to register

    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class TestSessionDetailAPIView(generics.RetrieveAPIView):
    queryset = TestSession.objects.all()
    serializer_class = TestSessionSerializer
    lookup_field = 'id'
