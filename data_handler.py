import json
import os  # Для проверки существования файла


base_path = os.path.abspath(os.path.dirname(__file__))
filename = os.path.join(base_path, "json/character.json")
# Функция для загрузки или создания персонажа
def load_or_create_character(filename=filename):

    

    # Проверяем, существует ли файл с персонажем
    if os.path.exists(filename):
        # Если файл есть, загружаем данные
        with open(filename, "r") as file:
            character = json.load(file)
        print("Персонаж успешно загружен.")
    else:
        # Если файла нет, создаём нового персонажа
        character = {
            "name": "Platon",
            "strength": 1,
            "endurance": 1,
            "level": 1,
            "experience": 0,
            "money": 0,
            "items": [],
            "equipped": {
                "armor": '',
                "helmet": '',
                "gloves": '',
                "boots": '',
                "pants": '',
                "weapon": '',
                "shield": '',
                "axe": '',
            },
            "win": 0,
            "loss": 0,
            "schutz": 0,
            "image": "images/knight.png"
        }
        with open(filename, "w") as file:
            json.dump(character, file, indent=4, ensure_ascii=False)
        print("Файл персонажа отсутствует. Создан новый персонаж.")
    return character