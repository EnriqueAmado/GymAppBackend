from .models import Exercise, Routine, RoutineExercise, WorkoutLog
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class GymFacade:

    # --- LÓGICA DE USUARIOS Y AUTENTICACIÓN (NUEVO) ---
    @staticmethod
    def register_user(username, email, password):
        """Crea un usuario en la BD de forma segura (contraseña encriptada)."""
        if User.objects.filter(username=username).exists():
            return None, "El nombre de usuario ya existe"
        user = User.objects.create_user(username=username, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return token.key, None

    @staticmethod
    def authenticate_user(username, password):
        """Verifica credenciales y retorna el Token si es válido."""
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return token.key, None
        return None, "Credenciales inválidas"

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



# ENDPOINTS DE LA API (AQUÍ ES DONDE RETROFIT LLAMARÁ DESDE ANDROID)

@api_view(['POST'])
def api_register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password or not email:
        return Response({'error': 'Todos los campos son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

    # Llamamos a nuestra fachada limpia
    token_key, error_msg = GymFacade.register_user(username, email, password)

    if error_msg:
        return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'token': token_key, 'username': username}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def api_login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Usuario y contraseña obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

    # Llamamos a nuestra fachada limpia
    token_key, error_msg = GymFacade.authenticate_user(username, password)

    if error_msg:
        return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'token': token_key, 'username': username}, status=status.HTTP_200_OK)