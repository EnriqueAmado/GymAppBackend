from django.contrib import admin
from .models import Exercise, Routine, RoutineExercise, WorkoutLog

# Registramos los modelos para que aparezcan en el panel /admin
admin.site.register(Exercise)
admin.site.register(Routine)
admin.site.register(RoutineExercise)
admin.site.register(WorkoutLog)
# Register your models here.
