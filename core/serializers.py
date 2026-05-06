from rest_framework import serializers
from .models import Exercise, Routine, RoutineExercise, WorkoutLog


# 1. Serializador de Ejercicios
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


# 2. Serializador del detalle de ejercicios dentro de una rutina
class RoutineExerciseSerializer(serializers.ModelSerializer):
    # Esto es para que en el JSON salga el nombre del ejercicio y no solo el ID
    exercise_name = serializers.ReadOnlyField(source='exercise.name')

    class Meta:
        model = RoutineExercise
        fields = ['id', 'exercise', 'exercise_name', 'sets', 'reps', 'order']


# 3. Serializador de Rutinas (Cabecera + Lista de ejercicios)
class RoutineSerializer(serializers.ModelSerializer):
    # Anidamos los ejercicios para que Android reciba la rutina completa de golpe
    exercises = RoutineExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Routine
        fields = ['id', 'name', 'created_at', 'exercises']


# 4. Serializador para los Logs (Progreso)
class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = ['id', 'exercise', 'date', 'weight', 'reps']