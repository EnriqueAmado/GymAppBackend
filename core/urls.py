from django.urls import path
from . import facade_v2
from .views import ExerciseListView, WorkoutLogCreateView

urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('logs/', WorkoutLogCreateView.as_view(), name='log-create'),
    path('register/', facade_v2.api_register_user, name='register_user'),
    path('login/', facade_v2.api_login_user, name='login_user'),
    path('routines/', facade_v2.api_routines, name='api_routines'),
    path('routine-exercises/', facade_v2.api_add_exercise_to_routine, name='api_add_exercise_to_routine'),
    path('workout-logs/', facade_v2.api_workout_logs, name='api_workout_logs'),
    path('routines/<int:pk>/delete/', facade_v2.api_delete_routine, name='api_delete_routine'),
    path('routine-exercises/<int:pk>/delete/', facade_v2.api_delete_routine_exercise, name='api_delete_routine_exercise'),
    path('progress/<int:exercise_id>/', facade_v2.api_get_progress, name='api_get_progress'),
    path('workout-logs/<int:pk>/delete/', facade_v2.api_delete_workout_log, name='api_delete_workout_log'),
]
