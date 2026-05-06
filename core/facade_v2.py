from .models import Exercise, Routine, RoutineExercise, WorkoutLog
from django.contrib.auth.models import User

class GymFacade:

    # --- LÓGICA DE EJERCICIOS ---
    @staticmethod
    def get_all_exercises():
        """Retorna todos los ejercicios del catálogo."""
        return Exercise.objects.all()

    @staticmethod
    def get_exercise_by_id(exercise_id):
        return Exercise.objects.filter(id=exercise_id).first()

    # --- LÓGICA DE RUTINAS ---
    @staticmethod
    def get_user_routines(user):
        """Retorna las rutinas de un usuario específico."""
        return Routine.objects.filter(user=user).prefetch_related('exercises__exercise')

    @staticmethod
    def create_routine(user, name):
        """Crea una nueva rutina vacía."""
        return Routine.objects.create(user=user, name=name)

    @staticmethod
    def add_exercise_to_routine(routine_id, exercise_id, sets, reps, order):
        """Añade un ejercicio a una rutina existente."""
        routine = Routine.objects.get(id=routine_id)
        exercise = Exercise.objects.get(id=exercise_id)
        return RoutineExercise.objects.create(
            routine=routine,
            exercise=exercise,
            sets=sets,
            reps=reps,
            order=order
        )

    # --- LÓGICA DE ENTRENAMIENTO (LOGS) ---
    @staticmethod
    def create_workout_log(user, exercise_id, weight, reps):
        """Registra una serie realizada por el usuario."""
        exercise = Exercise.objects.get(id=exercise_id)
        return WorkoutLog.objects.create(
            user=user,
            exercise=exercise,
            weight=weight,
            reps=reps
        )

    @staticmethod
    def get_user_progress(user, exercise_id):
        """Retorna el historial de un ejercicio para las gráficas."""
        return WorkoutLog.objects.filter(
            user=user,
            exercise_id=exercise_id
        ).order_by('date')