from tkinter import *
import json
from data_handler import load_or_create_character
import os


def items_window(return_to_main):
    root = Tk()

    root.geometry("1400x700")
    bg_color = "#452914"

    base_path = os.path.abspath(os.path.dirname(__file__))
    bg_image = os.path.join(base_path, 'images/inventory_bg.png')
    background_image = PhotoImage(file=(bg_image))
    background_image_label = Label(root, image=background_image)
    background_image_label.place(x=1, y=1)
    
    Label(root, text="Ваш инвентарь", font=("Arial", 16, "bold")).pack(pady=10)

    player = load_or_create_character()

    # Загружаем данные магазина из JSON
    try:
        with open("json/shop_items.json", "r", encoding="utf-8") as file:
            shop_items = json.load(file)
    except FileNotFoundError:
        shop_items = {}
        return

    def is_equipped(item_code):
        for category, items in shop_items.items():
            for item in items:
                if item["code"] == item_code:
                    # Проверяем соответствующую категорию
                    if category == "Шлемы" and player["equipped"]["helmet"] == item["name"]:
                        return True
                    elif category == "Броня" and player["equipped"]["armor"] == item["name"]:
                        return True
                    elif category == "Наручи" and player["equipped"]["gloves"] == item["name"]:
                        return True
                    elif category == "Сапоги" and player["equipped"]["boots"] == item["name"]:
                        return True
                    elif category == "Штаны" and player["equipped"]["pants"] == item["name"]:
                        return True
                    elif category == "Мечи" and player["equipped"]["weapon"] == item["name"]:
                        return True
                    elif category == "Щиты" and player["equipped"]["shield"] == item["name"]:
                        return True
                    elif category == "Топоры" and player["equipped"]["axe"] == item["name"]:
                        return True
        return False


    def equip_item(item_code):
        for category, items in shop_items.items():
            for item in items:
                if item["code"] == item_code:
                    # Для каждой категории добавляем логику проверки и экипировки
                    if category == "Шлемы" and not is_equipped(item_code):
                        if player["equipped"]["helmet"] != "":
                            old_helmet = player["equipped"]["helmet"]
                            for old_item in items:
                                if old_item["name"] == old_helmet:
                                    player["schutz"] -= old_item.get("defense", 0)
                                    break
                        player["equipped"]["helmet"] = item["name"]
                        player["schutz"] += item.get("defense", 0)

                    elif category == "Броня" and not is_equipped(item_code):
                        if player["equipped"]["armor"] != "":
                            old_armor = player["equipped"]["armor"]
                            for old_item in items:
                                if old_item["name"] == old_armor:
                                    player["schutz"] -= old_item.get("defense", 0)
                                    break
                        player["equipped"]["armor"] = item["name"]
                        player["schutz"] += item.get("defense", 0)

                    elif category == "Наручи" and not is_equipped(item_code):
                        if player["equipped"]["gloves"] != "":
                            old_gloves = player["equipped"]["gloves"]
                            for old_item in items:
                                if old_item["name"] == old_gloves:
                                    player["schutz"] -= old_item.get("defense", 0)
                                    break
                        player["equipped"]["gloves"] = item["name"]
                        player["schutz"] += item.get("defense", 0)

                    elif category == "Сапоги" and not is_equipped(item_code):
                        if player["equipped"]["boots"] != "":
                            old_boots = player["equipped"]["boots"]
                            for old_item in items:
                                if old_item["name"] == old_boots:
                                    player["schutz"] -= old_item.get("defense", 0)
                                    break
                        player["equipped"]["boots"] = item["name"]
                        player["schutz"] += item.get("defense", 0)

                    elif category == "Штаны" and not is_equipped(item_code):
                        if player["equipped"]["pants"] != "":
                            old_pants = player["equipped"]["pants"]
                            for old_item in items:
                                if old_item["name"] == old_pants:
                                    player["schutz"] -= old_item.get("defense", 0)
                                    break
                        player["equipped"]["pants"] = item["name"]
                        player["schutz"] += item.get("defense", 0)

                    elif category == "Щиты" and not is_equipped(item_code):
                        if player["equipped"]["shield"] != "":
                            old_shield = player["equipped"]["shield"]
                            for old_item in items:
                                if old_item["name"] == old_shield:
                                    player["schutz"] -= old_item.get("defense", 0)
                                    break
                        player["equipped"]["shield"] = item["name"]
                        player["schutz"] += item.get("defense", 0)

                    elif category == "Топоры" and not is_equipped(item_code):
                        if player["equipped"]["axe"] != "":
                            old_axe = player["equipped"]["axe"]
                            for old_item in items:
                                if old_item["name"] == old_axe:
                                    player["strength"] -= old_item.get("damage", 0)
                                    break
                        player["equipped"]["axe"] = item["name"]
                        player["strength"] += item.get("damage", 0)

                    elif category == "Мечи" and not is_equipped(item_code):
                        if player["equipped"]["weapon"] != "":
                            old_weapon = player["equipped"]["weapon"]
                            for old_item in items:
                                if old_item["name"] == old_weapon:
                                    player["strength"] -= old_item.get("damage", 0)
                                    break
                        player["equipped"]["weapon"] = item["name"]
                        player["strength"] += item.get("damage", 0)
                

        save_player_data()

    def unequip_item(item_code):
        for category, items in shop_items.items():
            for item in items:
                if item["code"] == item_code:
                    # Логика для каждой категории
                    if category == "Шлемы" and is_equipped(item_code):
                        player["equipped"]["helmet"] = ""
                        player["schutz"] -= item.get("defense", 0)

                    elif category == "Броня" and is_equipped(item_code):
                        player["equipped"]["armor"] = ""
                        player["schutz"] -= item.get("defense", 0)

                    elif category == "Наручи" and is_equipped(item_code):
                        player["equipped"]["gloves"] = ""
                        player["schutz"] -= item.get("defense", 0)

                    elif category == "Сапоги" and is_equipped(item_code):
                        player["equipped"]["boots"] = ""
                        player["schutz"] -= item.get("defense", 0)

                    elif category == "Штаны" and is_equipped(item_code):
                        player["equipped"]["pants"] = ""
                        player["schutz"] -= item.get("defense", 0)

                    elif category == "Щиты" and is_equipped(item_code):
                        player["equipped"]["shield"] = ""
                        player["schutz"] -= item.get("defense", 0)

                    elif category == "Топоры" and is_equipped(item_code):
                        player["equipped"]["axe"] = ""
                        player["strength"] -= item.get("damage", 0)

                    elif category == "Мечи" and is_equipped(item_code):
                        player["equipped"]["weapon"] = ""
                        player["strength"] -= item.get("damage", 0)
                

        save_player_data()

    def save_player_data():
        with open("json/character.json", "w", encoding="utf-8") as file:
            json.dump(player, file, indent=4, ensure_ascii=False)

    # Фрейм для отображения товаров
    content_frame = Frame(root, bg="#452914")
    content_frame.place(x=520, y=170)
    row = 0
    column = 0

    for item_code in player.get("items", []):
        for category, items in shop_items.items():
            for item in items:
                if item["code"] == item_code:
                    item_frame = Frame(content_frame, bg="#6f4221", padx=3, pady=3)  # Задаём фон и отступы
                    item_frame.grid(row=row, column=column, padx=10, pady=10)  # Размещение блока с отступами
                    # Параметры предмета
                    item_name = item.get("name", "Безымянный предмет")
                    item_defense = item.get("defense", 0)
                    item_damage = item.get("damage", 0)
                    item_image_path = item.get("image", "")
                    # Создаём контейнер для одного товара
                    item_frame = Frame(content_frame, bg="#6f4221", padx=3, pady=3)  # Задаём фон и отступы
                    item_frame.grid(row=row, column=column, padx=10, pady=10)  # Размещение блока с отступами

                    # Отображение фото предмета
                    try:
                        Label(item_frame,  text=f"{item_name}").grid(row=row, column=column)
                        item_photo = PhotoImage(file=item_image_path)  # Загружаем изображение из JSON
                        photo_label = Label(item_frame, bg=bg_color,image=item_photo)
                        photo_label.image = item_photo  # Сохраняем ссылку на изображение
                        photo_label.grid(row=row+1, column=column)
                        if "defense" in item:
                            Label(item_frame, text=f"Защита: {item_defense}").grid(row=row+2, column=column)
                        if "damage" in item:
                            Label(item_frame, text=f"Урон: {item_damage}").grid(row=row+3, column=column)
                        
                        
                    except Exception as e:
                        Label(content_frame, text=f"Не удалось загрузить изображение для {item_name}").grid(row=row, column=column)
                        print(e)


                    Button(
                        content_frame,
                        text="Надеть",
                        state="disabled" if is_equipped(item_code) else "normal",
                        command=lambda code=item_code: equip_item(code)
                    ).grid(row=row+4, column=column)


                    Button(
                        content_frame,
                        text="Снять",
                        state="normal" if is_equipped(item_code) else "disabled",
                        command=lambda code=item_code: unequip_item(code)
                    ).grid(row=row+5, column=column)

                    column += 1
                    if column > 5:  # Если больше 4 предметов в строке, переходим на следующий ряд
                        column = 0
                        row += 4

    Button(root, text="Вернуться в главное меню", command=lambda: go_back(root, return_to_main)).pack()

    root.mainloop()

def go_back(current_window, return_to_main):
    current_window.destroy()
    return_to_main()
