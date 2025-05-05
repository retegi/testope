import json
from applications.learning.models import Test  # Reemplaza 'yourapp' con el nombre de tu aplicación

# Ruta al archivo JSON
json_file_path = "bat_preguntas.json"

# Cargar datos desde el JSON
with open(json_file_path, "r", encoding="utf-8") as file:
    questions_data = json.load(file)

# Insertar los datos en la base de datos
for item in questions_data:
    Test.objects.create(
        number=item["question_number"],
        question=item["question_text"],
        aAnswer=item["options"]["a"],
        bAnswer=item["options"]["b"],
        cAnswer=item["options"]["c"],
        dAnswer=item["options"]["d"]
    )

print("✅ Preguntas importadas correctamente.")
