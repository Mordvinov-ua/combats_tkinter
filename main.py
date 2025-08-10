from tkinter import *
from fight import battle_window
from shop import shop_window
from data_handler import load_or_create_character
from inventar import items_window
import os
import json

def main_page():
    character = load_or_create_character()

    # Загружаем данные магазина из JSON
    try:
        with open("json/shop_items.json", "r", encoding="utf-8") as file:
            shop_items = json.load(file)
    except FileNotFoundError:
        shop_items = {}
        return

    root = Tk()
    root.title("Главное меню")
    root.geometry("1400x700")

    base_path = os.path.abspath(os.path.dirname(__file__))
    bg_image = os.path.join(base_path, 'images/background.png')
    background_image = PhotoImage(file=(bg_image))
    background_image_label = Label(root, image=background_image)
    background_image_label.place(x=1, y=1)
        

    # Добавляем фото персонажа
    try:
        character_image = PhotoImage(file=(f"images/{character['image']}{character['level']}.png"))  # Путь загружается из JSON
        image_label = Label(root, image=character_image)
        image_label.image = character_image  # Сохраняем ссылку на изображение, чтобы избежать его очистки сборщиком мусора
        image_label.place(x=1120, y=70)
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")

    # Словарь с настройками для каждого слота экипировки.
    # Для каждого слота указываются:
    # - Координаты размещения (x и y)
    # - Путь к изображению по умолчанию, если предмет не экипирован или его не удалось загрузить.
    equipment_slots = {
        "armor":   {"x": 1295, "y": 70,  "default": os.path.join(base_path, 'images/leer_armor.png')},
        "pants":    {"x": 1295, "y": 135, "default": os.path.join(base_path, 'images/hoze_leer.png')},
        "shield":  {"x": 1295, "y": 200, "default": os.path.join(base_path, 'images/schild_leer.png')},
        "boots":   {"x": 1295, "y": 265, "default": os.path.join(base_path, 'images/boots_leer.png')},
        "helmet":  {"x": 1075, "y": 70,  "default": os.path.join(base_path, 'images/helm_leer.png')},
        "gloves":  {"x": 1075, "y": 135, "default": os.path.join(base_path, 'images/gloves_leer.png')},
        "weapon":   {"x": 1075, "y": 200, "default": os.path.join(base_path, 'images/waffe_leer.png')},
        "ring":    {"x": 1075, "y": 265, "default": os.path.join(base_path, 'images/ring_leer.png')}
    }

    # Функция поиска и загрузки изображения для заданного слота экипировки.
    def get_equipment_image(slot_name):
        equipped_item_name = character["equipped"].get(slot_name)
        if equipped_item_name:
            # Перебираем элементы магазина, чтобы найти предмет с нужным именем.
            found = False
            for category, category_items in shop_items.items():
                for shop_item in category_items:
                    if equipped_item_name == shop_item.get("name"):
                        image_path = shop_item.get("image", "")
                        try:
                            image = PhotoImage(file=image_path)
                        except Exception as e:
                            print(f"Ошибка загрузки изображения для {equipped_item_name}: {e}")
                            # Если произошла ошибка – используем изображение по умолчанию для данного слота
                            image = PhotoImage(file=equipment_slots[slot_name]["default"])
                        found = True
                        break
                if found:
                    break
            else:
                # Если предмет не найден – используем изображение по умолчанию.
                image = PhotoImage(file=equipment_slots[slot_name]["default"])
        else:
            # Если ничего не экипировано в данном слоте – используем изображение по умолчанию.
            image = PhotoImage(file=equipment_slots[slot_name]["default"])
        return image

    # Отображаем экипировку персонажа
    for slot, info in equipment_slots.items():
        slot_image = get_equipment_image(slot)
        label = Label(root, image=slot_image)
        label.image = slot_image  # сохраняем ссылку, чтобы изображение не удалилось сборщиком мусора
        label.place(x=info["x"], y=info["y"], width=60, height=60)

    # Отображение параметров персонажа
    Label(root, text=f"{character['name']}", font=("Arial", 16, "bold")).place(x=1180, y=1)
    Label(root, text=f"Сила: {character['strength']}", font=("Comic Sans MS", 14)).place(x=1155, y=320)
    Label(root, text=f"Выносливость: {character['endurance']}", font=("Comic Sans MS", 14)).place(x=1155, y=345)
    Label(root, text=f"Уровень: {character['level']}", font=("Arial", 16, "bold")).place(x=1155, y=25)
    Label(root, text=f"Опыт: {character['experience']}").place(x=1180, y=50)
    Label(root, text=f"Защита: {character['schutz']}", font=("Comic Sans MS", 14)).place(x=1155, y=370)
    Label(root, text=f"Победы: {character['win']}").place(x=1155, y=400)
    Label(root, text=f"Поражения: {character['loss']}").place(x=1155, y=420)
    Label(root, text=f"Деньги: {character['money']}").place(x=1155, y=440)

    Button(root, text="Лес", width=6, bg="#886c3a", fg="#221b11", font=("Comic Sans MS", 14), activebackground="#a58b50",
                   activeforeground="#221b11", command=lambda: wald_fight(root)).place(x=624, y=379)
    Button(root, text="Магазин", bg="#886c3a", fg="#221b11", font=("Comic Sans MS", 14), activebackground="#a58b50",
                   activeforeground="#221b11", command=lambda: shop(root)).place(x=235, y=430)
    

    load_invent_image = os.path.join(base_path, 'images/chest.png')
    inventory_image = PhotoImage(file=(load_invent_image))
    background_image_label = Label(root, image=inventory_image)
    background_image_label.place(x=1135, y=510)
    Button(root, text="Инвентарь", bg="#886c3a", fg="#221b11", font=("Comic Sans MS", 14), activebackground="#a58b50",
                   activeforeground="#221b11", command=lambda: items_page(root)).place(x=1155, y=640)

    root.mainloop()

def wald_fight(current_window):
    current_window.destroy()
    battle_window(main_page)  # Передаем функцию возврата

def shop(current_window):
    current_window.destroy()
    shop_window(main_page)  # Передаем функцию возврата

def items_page(current_window):
    current_window.destroy()
    items_window(main_page)

main_page()