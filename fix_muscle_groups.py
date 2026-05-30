import os
import django
import sys

# Configurar el entorno de Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Exercise

# Diccionario de mapeo de nombres a grupos musculares
mapping = {
    "Pecho": ["Press de Banca", "Aperturas"],
    "Pierna": ["Sentadilla", "Prensa", "Extensiones de Cuádriceps", "Curl Femoral", "Zancadas", "Elevación de Gemelos"],
    "Espalda": ["Dominadas", "Remo", "Jalón al Pecho", "Peso Muerto"],
    "Hombro": ["Press Militar", "Elevaciones Laterales", "Pájaros"],
    "Bíceps": ["Curl de Bíceps", "Curl Martillo"],
    "Tríceps": ["Extensión de Tríceps", "Fondos de Tríceps"],
    "Abdominales": ["Plancha", "Crunch"]
}

print("Actualizando grupos musculares...")

exercises = Exercise.objects.all()
for ex in exercises:
    found = False
    for group, keywords in mapping.items():
        for keyword in keywords:
            if keyword.lower() in ex.name.lower():
                ex.body_part = group
                ex.save()
                print(f"✅ {ex.name} -> {group}")
                found = True
                break
        if found: break

    if not found:
        # Fallback si no coincide nada
        if "curl" in ex.name.lower():
            ex.body_part = "Bíceps"
        elif "press" in ex.name.lower():
            ex.body_part = "Pecho"
        else:
            ex.body_part = "Otros"
        ex.save()
        print(f"❓ {ex.name} -> {ex.body_part} (Asignado por defecto)")

print("¡Proceso completado!")
