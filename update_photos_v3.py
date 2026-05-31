import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Exercise

# URLs directas de Wikimedia (formato original, sin redimensionar para evitar 404)
photos = {
    "Press de Banca con Barra": "https://upload.wikimedia.org/wikipedia/commons/0/08/Bench-press-1.png",
    "Sentadilla Trasera con Barra": "https://upload.wikimedia.org/wikipedia/commons/8/82/Squats.png",
    "Dominadas": "https://upload.wikimedia.org/wikipedia/commons/e/ee/Pullup-1.png",
    "Peso Muerto Convencional": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Deadlift.png",
    "Curl de Bíceps con Barra EZ": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Biceps-curl-1.png"
}

print("Actualizando a URLs definitivas de Wikimedia...")

for name, url in photos.items():
    Exercise.objects.filter(name=name).update(image_url=url)
    print(f"✅ Foto asignada a: {name}")

print("¡Listo! Cierra la App y vuelve a entrar.")
