from django.urls import path
from apps.quiz.views.solution_views import QuizSolutionView, QuizSolutionDetailView
from apps.quiz.views.group_views import QuizGroupView, QuizGroupDetailView
from apps.quiz.views.quiz_views import QuizDetailView, QuizView

urlpatterns = [
    path('courses/<uuid:course_id>/quiz-solutions/', QuizSolutionView.as_view()),
    path('quiz-solutions/<str:solution_id>/', QuizSolutionDetailView.as_view()),

    path('courses/<uuid:course_id>/quiz-groups/', QuizGroupView.as_view()),
    path('quiz-groups/<str:group_id>/', QuizGroupDetailView.as_view()),

    path('quiz-groups/<str:group_id>/quizzes/', QuizView.as_view()),
    path('quizzes/<uuid:quiz_id>/', QuizDetailView.as_view()),
]
