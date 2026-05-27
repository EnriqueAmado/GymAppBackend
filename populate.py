import os
import django
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Exercise

ejercicios = [
    ("Press de Banca", "Pecho"), ("Press Inclinado", "Pecho"), ("Aperturas", "Pecho"),
    ("Sentadilla", "Pierna"), ("Prensa", "Pierna"), ("Extensiones", "Pierna"),
    ("Dominadas", "Espalda"), ("Remo con Barra", "Espalda"), ("Jalón al pecho", "Espalda"),
    ("Press Militar", "Hombro"), ("Elevaciones Laterales", "Hombro"),
    ("Curl de Bíceps", "Brazo"), ("Extensión de Tríceps", "Brazo")
]
print("Iniciando carga de ejercicios...")
for nombre, musculo in ejercicios:
    obj, created = Exercise.objects.get_or_create(name=nombre, body_part=musculo)
    if created:
        print(f" Añadido: {nombre}")
    else:
        print(f" Ya existía: {nombre}")
    print("Proceso terminado")