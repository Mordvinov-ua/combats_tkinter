from tkinter import *
import json
import os

def shop_window(return_to_main):
    shop = Tk()
    bg_color = "#452914"
    shop.configure(bg=bg_color)
    shop.title("Магазин")
    shop.geometry("1400x700")
    

    base_path = os.path.abspath(os.path.dirname(__file__))
    bg_image = os.path.join(base_path, 'images/shop_pg.png')
    background_image = PhotoImage(file=(bg_image))
    background_image_label = Label(shop, image=background_image)
    background_image_label.place(x=1, y=1)


    # Загружаем данные игрока
    try:
        with open("json/character.json", "r", encoding="utf-8") as file:
            player = json.load(file)
    except FileNotFoundError:
        player = {}
        print("Ошибка: файл player.json не найден.")

    # Загружаем данные магазина из JSON
    try:
        with open("json/shop_items.json", "r", encoding="utf-8") as file:
            shop_items = json.load(file)
    except FileNotFoundError:
        shop_items = {}
        print("Ошибка: файл shop_items.json не найден.")

    def buy_item(item):
        item_price = item.get("price", 0)
        if player["money"] >= item_price:
            player["money"] -= item_price
            player["items"].append(item["code"])  # Добавляем код предмета в инвентарь

            # Обновление файла игрока
            with open("json/character.json", "w", encoding="utf-8") as file:
                json.dump(player, file, indent=4, ensure_ascii=False)

            Label(content_frame, text=f"Вы купили {item['name']}!")
        else:
            Label(content_frame, text="Недостаточно денег для покупки.")

    def show_category(category):
        # Очистка текущего содержимого окна
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Отображение товаров из выбранной категории
        items = shop_items.get(category, [])
        '''Label(content_frame,text=f"Товары в категории: {category}").grid(row=0, column=0, columnspan=4)'''
        row=0
        column = 0

        for item in items:
            # Параметры предмета
            item_name = item.get("name", "Безымянный предмет")
            item_defense = item.get("defense", 0)
            item_damage = item.get("damage", 0)
            item_price = item.get("price", 0)
            item_image_path = item.get("image", "")
            # Создаём контейнер для одного товара
            item_frame = Frame(content_frame, bg="#6f4221", padx=3, pady=3)  # Задаём фон и отступы
            item_frame.grid(row=row, column=column, padx=10, pady=10)  # Размещение блока с отступами

            # Отображение фото предмета
            try:
                item_photo = PhotoImage(file=item_image_path)  # Загружаем изображение из JSON
                photo_label = Label(item_frame, bg=bg_color,image=item_photo)
                photo_label.image = item_photo  # Сохраняем ссылку на изображение
                photo_label.grid(row=row, column=column)
                Button(item_frame, text="Купить", command=lambda item=item: buy_item(item)).grid(row=row+1, column=column)
                column += 1
                Label(item_frame,  text=f"{item_name}").grid(row=row, column=column)
                if "defense" in item:
                    Label(item_frame, text=f"Защита: {item_defense}").grid(row=row+1, column=column)
                if "damage" in item:
                    Label(item_frame, text=f"Урон: {item_damage}").grid(row=row+2, column=column)
                Label(item_frame,  text=f"Цена: {item_price}").grid(row=row+3, column=column)
                
                
            except Exception as e:
                Label(content_frame, text=f"Не удалось загрузить изображение для {item_name}").grid(row=row, column=column)
                print(e)

            column += 1
            if column > 5:  # Если больше 4 предметов в строке, переходим на следующий ряд
                column = 0
                row += 4
            

    # Выпадающее меню для выбора категорий
    selected_category = StringVar(shop)
    selected_category.set("Выберите категорию")
    categories_menu = OptionMenu(shop,selected_category, *shop_items.keys(), command=show_category)
    categories_menu.place(x=250, y=120)

    # Фрейм для отображения товаров
    content_frame = Frame(shop, bg="#452914")
    content_frame.place(x=110, y=210)

    Button(shop, text="Вернуться в город", command=lambda: go_back(shop, return_to_main)).place(x=450, y=120)

    shop.mainloop()

def go_back(current_window, return_to_main):
    current_window.destroy()
    return_to_main()