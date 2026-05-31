import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Exercise

# Diccionario de fotos (URLs de Wikipedia/Wikimedia de uso libre)
photos = {
    "Press de Banca con Barra": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Bench-press-1.png/800px-Bench-press-1.png",
    "Sentadilla Trasera con Barra": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Squats.png/800px-Squats.png",
    "Dominadas": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Pullup-1.png/800px-Pullup-1.png",
    "Peso Muerto Convencional": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Deadlift.png/800px-Deadlift.png",
    "Curl de Bíceps con Barra EZ": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Biceps-curl-1.png/800px-Biceps-curl-1.png"
}

print("Asignando fotos a los ejercicios...")

for name, url in photos.items():
    Exercise.objects.filter(name=name).update(image_url=url)
    print(f"📷 Foto añadida a: {name}")

print("¡Listo! Ya puedes ver las fotos en la App.")
