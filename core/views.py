from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .facade_v2 import GymFacade
from .serializers import ExerciseSerializer, RoutineSerializer, WorkoutLogSerializer


# Vista para obtener el catálogo de ejercicios
class ExerciseListView(APIView):
    def get(self, request):
        exercises = GymFacade.get_all_exercises()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)


# Vista para las Rutinas del usuario
class RoutineListView(APIView):
    def get(self, request):
        # Por ahora usamos el usuario 1 (admin) para probar.
        # Luego lo cambiaremos por el usuario logueado en Android.
        from django.contrib.auth.models import User
        user = User.objects.get(id=1)

        routines = GymFacade.get_user_routines(user)
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data)


# Vista para registrar un levantamiento (WorkoutLog)
class WorkoutLogCreateView(APIView):
    def post(self, request):
        from django.contrib.auth.models import User
        user = User.objects.get(id=1)  # Prototipo rápido

        data = request.data
        try:
            log = GymFacade.create_workout_log(
                user=user,
                exercise_id=data.get('exercise'),
                weight=data.get('weight'),
                reps=data.get('reps')
            )
            serializer = WorkoutLogSerializer(log)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
