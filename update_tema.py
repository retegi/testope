

import django
import os

# Configurar el entorno de Django (ajusta esto si es necesario)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tu_proyecto.settings")
django.setup()

from applications.learning.models import Test, Topic

# Definir el tema
tema_texto = "TEMA 3. EL MUNICIPIO. LA ORGANIZACIÓN MUNICIPAL DE LOS MUNICIPIOS DE GRAN POBLACIÓN (TÍTULO X DE LA LEY 7/1985, DE 2 DE ABRIL, REGULADORA DE LAS BASES DEL RÉGIMEN LOCAL)."

# Obtener o crear el tema en la tabla Topic
tema_obj, created = Topic.objects.get_or_create(name=tema_texto)

# Actualizar los registros de Test donde number está entre 1 y 35
tests_actualizados = Test.objects.filter(number__gte=71, number__lte=105).update(topic=tema_obj)

print(f"✅ Se han actualizado {tests_actualizados} registros con el tema: {tema_texto}")
