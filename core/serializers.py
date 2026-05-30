from rest_framework import serializers
from .models import Exercise, Routine, RoutineExercise, WorkoutLog


# Serializador de Ejercicios
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


# Serializador del detalle de ejercicios dentro de una rutina
class RoutineExerciseSerializer(serializers.ModelSerializer):
    routine = serializers.PrimaryKeyRelatedField(queryset=Routine.objects.all())
    exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all())

    # Creamos este campo dinámico de solo lectura que viaja al modelo Exercise
    # y saca el nombre. Así no rompe el POST desde Android y te da el dato en el GET.
    exercise_name = serializers.ReadOnlyField(source='exercise.name')

    class Meta:
        model = RoutineExercise
        # Incluimos tanto 'routine' (vital para el POST) como 'exercise_name' (vital para el GET)
        fields = ['id', 'routine', 'exercise', 'exercise_name', 'sets', 'reps', 'order']


#  Serializador de Rutinas (Cabecera + Lista de ejercicios)
class RoutineSerializer(serializers.ModelSerializer):
    # Anidamos los ejercicios usando el related_name='exercises'
    exercises = RoutineExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Routine
        fields = ['id', 'name', 'created_at', 'exercises']


#  Serializador para los Logs (Progreso)
class WorkoutLogSerializer(serializers.ModelSerializer):
    exercise_name = serializers.ReadOnlyField(source='exercise.name')
    created_at = serializers.DateField(source='date', read_only=True)

    class Meta:
        model = WorkoutLog
        fields = ['id', 'exercise', 'exercise_name', 'created_at', 'weight', 'reps']
