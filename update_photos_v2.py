import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Exercise

# Nuevas URLs de imágenes más estables
photos = {
    "Press de Banca con Barra": "https://www.entrenamientos.com/media/cache/exercise_375/exercises/2-1-press-de-banca-con-barra-7117.png",
    "Sentadilla Trasera con Barra": "https://www.entrenamientos.com/media/cache/exercise_375/exercises/5-1-sentadilla-trasera-con-barra-1144.png",
    "Dominadas": "https://www.entrenamientos.com/media/cache/exercise_375/exercises/6-2-dominadas-en-barra-fija-pronacion-3564.png",
    "Peso Muerto Convencional": "https://www.entrenamientos.com/media/cache/exercise_375/exercises/1-1-peso-muerto-con-barra-4752.png",
    "Curl de Bíceps con Barra EZ": "https://www.entrenamientos.com/media/cache/exercise_375/exercises/10-1-curl-de-biceps-con-barra-ez-2591.png"
}

print("Actualizando a URLs de imagen compatibles...")

for name, url in photos.items():
    Exercise.objects.filter(name=name).update(image_url=url)
    print(f"✅ URL actualizada para: {name}")

print("¡Listo! Prueba a entrar de nuevo en la App.")
