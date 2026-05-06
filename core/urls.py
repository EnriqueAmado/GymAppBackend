from django.urls import path
from .views import ExerciseListView, RoutineListView, WorkoutLogCreateView

urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('routines/', RoutineListView.as_view(), name='routine-list'),
    path('logs/', WorkoutLogCreateView.as_view(), name='log-create'),
]