
from django.db import models
from django.contrib.auth.models import User

# 1. Catálogo de Ejercicios
class Exercise(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del Ejercicio")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    body_part = models.CharField(max_length=50, verbose_name="Grupo Muscular") # Ej: Pecho, Espalda...

    def __str__(self):
        return self.name

# 2. Rutinas (Cabecera)
class Routine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routines')
    name = models.CharField(max_length=100, verbose_name="Nombre de la Rutina")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

# 3. Ejercicios dentro de una Rutina (Detalle)
class RoutineExercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(default=3)
    reps = models.IntegerField(default=10)
    order = models.IntegerField(default=0) # Para que en Android aparezcan en orden (1º, 2º...)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.exercise.name} en {self.routine.name}"

# 4. Registro de Entrenamiento (WorkoutLog) -> Para las gráficas de progreso
class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True) # Se pone la fecha de hoy automáticamente
    weight = models.DecimalField(max_digits=5, decimal_places=2) # Soporta hasta 999.99 kg
    reps = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.exercise.name} - {self.weight}kg"
# Create your models here.
