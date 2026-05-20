from django.urls import path
from . import facade_v2
from .views import ExerciseListView, RoutineListView, WorkoutLogCreateView

urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('routines/', RoutineListView.as_view(), name='routine-list'),
    path('logs/', WorkoutLogCreateView.as_view(), name='log-create'),
    path('register/', facade_v2.api_register_user, name='register_user'),
    path('login/', facade_v2.api_login_user, name='login_user'),
]