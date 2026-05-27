from .models import Exercise, Routine, RoutineExercise, WorkoutLog
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class GymFacade:

    # --- LÓGICA DE USUARIOS Y AUTENTICACIÓN ---
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


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_routines(request):
    """
    GET: Devuelve todas las rutinas del usuario logueado con sus ejercicios.
    POST: Crea una rutina para el usuario logueado.
    """
    user = request.user

    if request.method == 'GET':
        # Obtenemos las rutinas
        routines = GymFacade.get_user_routines(user)

        # Construimos un JSON para evitar líos de Serializers complejos
        response_data = []
        for r in routines:
            # Buscamos los ejercicios asignados a esta rutina (los detalles de las series)
            exercises_in_routine = []
            for re in r.exercises.all():
                exercises_in_routine.append({
                    'id': re.id,
                    'exercise_name': re.exercise.name,
                    'body_part': re.exercise.body_part,
                    'sets': re.sets,
                    'reps': re.reps,
                    'order': re.order
                })

            response_data.append({
                'id': r.id,
                'name': r.name,
                'created_at': r.created_at.strftime('%Y-%m-%d'),
                'exercises': exercises_in_routine
            })

        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        name = request.data.get('name')
        if not name:
            return Response({'error': 'El nombre de la rutina es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

        # Creamos la rutina vacía usando la fachada
        new_routine = GymFacade.create_routine(user, name)

        # Si en la petición vienen ejercicios metidos de golpe, los añadimos
        exercises_list = request.data.get('exercises', [])
        for item in exercises_list:
            GymFacade.add_exercise_to_routine(
                routine_id=new_routine.id,
                exercise_id=item.get('exercise_id'),
                sets=item.get('sets', 3),
                reps=item.get('reps', 10),
                order=item.get('order', 0)
            )

        return Response({
            'id': new_routine.id,
            'name': new_routine.name,
            'message': 'Rutina creada con éxito'
        }, status=status.HTTP_201_CREATED)


# 🌟 CORREGIDO: Eliminados los espacios iniciales para que Django lo lea como función global del módulo
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_add_exercise_to_routine(request):
    """
    POST: Recibe los datos de Android (routine, exercise, sets, reps, order)
    y los inserta en la tabla intermedia a través de la Fachada.
    """
    data = request.data

    # Recuperamos los parámetros que vienen del RoutineExerciseRequest de Android
    routine_id = data.get('routine')
    exercise_id = data.get('exercise')
    sets = data.get('sets')
    reps = data.get('reps')
    order = data.get('order')

    # Validamos que Android nos mande todos los campos obligatorios
    if not all([routine_id, exercise_id, sets, reps, order]):
        return Response(
            {'error': 'Faltan campos obligatorios en la petición'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Reutilizamos el metodo de la fachada
        routine_exercise = GymFacade.add_exercise_to_routine(
            routine_id=int(routine_id),
            exercise_id=int(exercise_id),
            sets=int(sets),
            reps=int(reps),
            order=int(order)
        )

        # Respondemos con éxito absoluto (HTTP 201 Created)
        return Response({
            'id': routine_exercise.id,
            'message': 'Ejercicio asociado con éxito a la rutina',
            'routine_id': routine_id,
            'exercise_name': routine_exercise.exercise.name
        }, status=status.HTTP_201_CREATED)

    except Routine.DoesNotExist:
        return Response({'error': 'La rutina especificada no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exercise.DoesNotExist:
        return Response({'error': 'El ejercicio especificado no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_save_workout_log(request):
    try:
        # Recuperamos los datos que nos manda Android en el JSON
        routine_exercise_id = request.data.get('routine_exercise')
        weight = request.data.get('weight')
        reps = request.data.get('reps')

        if not routine_exercise_id or weight is None or reps is None:
            return Response({"error": "Faltan campos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)

        # Buscamos la relación intermedia del ejercicio en la rutina
        try:
            routine_exercise = RoutineExercise.objects.get(id=routine_exercise_id)
        except RoutineExercise.DoesNotExist:
            return Response({"error": "La rutina-ejercicio no existe"}, status=status.HTTP_404_NOT_FOUND)

        # Creamos y guardamos el Log en la Base de Datos enlazado al usuario del Token
        workout_log = WorkoutLog.objects.create(
            user=request.user,  # Django saca el usuario directamente del Token de forma segura
            exercise=routine_exercise.exercise,
            weight=weight,
            reps=reps
        )

        return Response({"message": "Serie guardada con éxito", "id": workout_log.id}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- LÓGICA DE ELIMINACIÓN ---
@staticmethod
def delete_routine(user, routine_id):
    """Elimina una rutina completa del usuario."""
    routine = Routine.objects.get(id=routine_id, user=user)
    routine.delete()  # Como tienes CASCADE, esto borrará sus RoutineExercise automáticamente.

@staticmethod
def delete_exercise_from_routine(user, routine_exercise_id):
    """Elimina un ejercicio específico dentro de una rutina."""
    routine_exercise = RoutineExercise.objects.get(id=routine_exercise_id, routine__user=user)
    routine_exercise.delete()

    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_delete_routine(request, pk):
    """Elimina una rutina por su ID (Primary Key)."""
    try:
        GymFacade.delete_routine(request.user, pk)
        return Response({'message': 'Rutina eliminada con éxito'}, status=status.HTTP_200_OK)
    except Routine.DoesNotExist:
        return Response({'error': 'La rutina no existe o no te pertenece'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_delete_routine_exercise(request, pk):
    """Elimina un ejercicio de una rutina por su ID intermedio."""
    try:
        GymFacade.delete_exercise_from_routine(request.user, pk)
        return Response({'message': 'Ejercicio eliminado de la rutina con éxito'}, status=status.HTTP_200_OK)
    except RoutineExercise.DoesNotExist:
        return Response({'error': 'El ejercicio no existe en esta rutina o no te pertenece'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)