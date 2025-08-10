from tkinter import *
import random
import json
import os

monster_suche_count = 0

def battle_window(return_to_main):
    root = Tk()
    bg_color = "#59520e"
    root.configure(bg=bg_color)

    root.geometry("1400x700")

    base_path = os.path.abspath(os.path.dirname(__file__))
    bg_image = os.path.join(base_path, 'images/new_wald_bg.png')
    background_image = PhotoImage(file=(bg_image))
    background_image_label = Label(root, image=background_image)
    background_image_label.place(x=1, y=1)
    random_funk = ''
    x = ''
    result = ''

    def calculate_health_bar_damage(max_health, damage):
        # Вычисляем процент урона
        damage_percentage = (damage / max_health)
        # Преобразуем в урон по полоске здоровья
        bar_damage = round(damage_percentage * 20)
        return bar_damage
    
    def calculate_damage_per_unit(schutz):
        damage_per_unit = 20 / schutz
        return round(damage_per_unit)


    def start():
        funk = ('-', '+')
        global random_funk
        random_funk = random.choice(funk)
        if random_funk == '-':
            global result
            result = random.randint(10, 93)
            global x
            x = random.randint(result + 6, 99)
            label_question.config(text=f"{x} {random_funk} ? = {result}")
        else:
            result = random.randint(26, 99)
            x = random.randint(8, result - 7)
            label_question.config(text=f"{x} {random_funk} ? = {result}")
        weiter_button.config(state=DISABLED)
        start_button.config(state=DISABLED)
        attack_button.config(state=NORMAL)
        go_home_button.config(state=DISABLED)
        

    def ergebnis(gegners_health, gegners_damage, gegners_schutz, users_health, users_damage, users_schutz, gegner):
        global random_funk
        global result
        global x
        with open("json/character.json", "r", encoding="utf-8") as file:
            player = json.load(file)
        user_antwort = entry.get()
        if not user_antwort.isdigit():
            users_damage = 5
            user_antwort = 0
        if random_funk == '-':
            ergebnis = int(x) - int(result)
        else:
            ergebnis = int(result) - int(x)
        

        if ergebnis == int(user_antwort):

            if schutz_p2['width'] > 0:
                shutz_point = calculate_damage_per_unit(gegner_schutz_bar)
                if schutz_p2['width'] >= (users_damage * shutz_point):
                    schutz_p2['width'] -= (users_damage * shutz_point)
                    users_damage = 0
                else:
                    schutz_p2['width'] = 0
                    schutz_p2['bg'] = '#d9d9d9'
                    users_damage = ((users_damage * shutz_point) - schutz_p2['width'])/shutz_point

            if users_damage > 0:       
                users_punch = random.randint(1,users_damage)
                hp_p2['width'] -= calculate_health_bar_damage(gegners_health, users_punch)
                if hp_p2['width'] <= 10 and hp_p2['width'] > 5:
                    hp_p2['bg'] = 'yellow'
                elif hp_p2['width'] <= 5:
                    hp_p2['bg'] = 'red'
                if hp_p2['width'] <= 0:
                    weiter_button.config(state=NORMAL)
                    start_button.config(state=DISABLED)
                    attack_button.config(state=DISABLED)
                    go_home_button.config(state=NORMAL)
                    hp_p2['bg'] = '#d9d9d9'
                    im_avatar_p2.config(file=('images/wald_krest.png'))
                    player["win"] += 1
                    # Обновление файла игрока
                    with open("json/character.json", "w", encoding="utf-8") as file:
                        json.dump(player, file, indent=4, ensure_ascii=False)
                    update_player_after_battle("json/character.json", gegner_xp, gegner_money)
                    with open("json/wald_monsters.json", "r", encoding="utf-8") as file:
                        monsters = json.load(file)
                    for monster in monsters:
                        if monster["name"] == gegner["name"]:
                            if monster["kill_count"] < 10:
                                monster["kill_count"] += 1
                                break
                            else:
                                monster["boss_kill"] += 1
                    
                    with open("json/wald_monsters.json", "w", encoding="utf-8") as file:
                        json.dump(monsters, file, indent=4, ensure_ascii=False)
                    return
                
        else:
            if schutz_p1['width'] > 0:
                shutz_point = calculate_damage_per_unit(player_schutz_bar)
                if schutz_p1['width'] >= (gegners_damage * shutz_point):
                    schutz_p1['width'] -= (gegners_damage * shutz_point)
                    gegners_damage = 0
                else:
                    schutz_p1['width'] = 0
                    schutz_p1['bg'] = '#d9d9d9'
                    gegners_damage = ((gegners_damage * shutz_point) - schutz_p1['width'])/shutz_point

            if gegners_damage > 0:       
                gegners_punch = random.randint(1,gegners_damage)
                hp_p1['width'] -= calculate_health_bar_damage(users_health, gegners_punch)
                if hp_p1['width'] <= 10 and hp_p1['width'] > 5 :
                    hp_p1['bg'] = 'yellow'
                if hp_p1['width'] <= 5:
                    hp_p1['bg'] = 'red'
                if hp_p1['width'] <= 0:
                    weiter_button.config(state=DISABLED)
                    start_button.config(state=DISABLED)
                    attack_button.config(state=DISABLED)
                    go_home_button.config(state=NORMAL)
                    hp_p1['bg'] = '#d9d9d9'
                    im_avatar_p1.config(file=('images/krest.png'))
                    player["loss"] += 1
                    # Обновление файла игрока
                    with open("json/character.json", "w", encoding="utf-8") as file:
                        json.dump(player, file, indent=4, ensure_ascii=False)
                    return
        entry.delete(0,END)
        start()
    
    def gegner_suche():
        start_button.config(state=NORMAL)
        entry.delete(0,END)
        # Загружаем данные игрока
        try:
            with open("json/character.json", "r", encoding="utf-8") as file:
                player = json.load(file)
        except FileNotFoundError:
            player = {}
            Label(root, text="Ошибка: файл player.json не найден.").pack()

        global player_health_bar, player_schutz_bar,player_attack_power, player_money, player_xp

        player_money = int(player["money"])
        player_xp = int(player["experience"])
        player_health_bar = 4 + int(player["endurance"])
        player_schutz_bar = int(player["schutz"])
        player_attack_power = int(player["strength"])

        im_avatar_p1.config(file=(f"images/wald_{player['image']}{player['level']}.png"))
        hp_p1.config(bg='green', height=1, width=20)
        if player_schutz_bar > 0:
            schutz_p1.config(bg='grey', height=1, width=20)
        else:
            schutz_p1.config(bg='#d9d9d9', height=0, width=0)

        # Загружаем данные protivnika

        try:
            with open("json/wald_monsters.json", "r", encoding="utf-8") as file:
                monsters = json.load(file)
        except FileNotFoundError:
            monsters = []
            Label(root, text="Ошибка: файл wald_monsters.json не найден.").pack()

        # Получение случайного персонажа

        if monsters:
            random_monster = random.choice(monsters)
        else:
            print("Список монстров пуст.")
    
        
        if random_monster["boss_kill"] > 0:
            global monster_suche_count
            monster_suche_count +=1
            if monster_suche_count > 15:
                Label(root, text="Список монстров пуст.").pack()
                return
            gegner_suche()
            return

        global gegner_health_bar, gegner_schutz_bar,gegner_attack_power, gegner_money, gegner_xp, gegner_object
        if random_monster["kill_count"] < 10:
            gegner_money = int(random_monster["money"])
            gegner_xp = int(random_monster["experience"])
            gegner_health_bar = int(random_monster["endurance"])
            gegner_schutz_bar = int(random_monster["schutz"])
            gegner_attack_power = int(random_monster["strength"])
            im_avatar_p2.config(file=(random_monster["image"]))
            
        else:
            gegner_money = int(random_monster["boss_money"])
            gegner_xp = int(random_monster["boss_experience"])
            gegner_health_bar = 3 + int(random_monster["boss_endurance"])
            gegner_schutz_bar = int(random_monster["boss_schutz"])
            gegner_attack_power = int(random_monster["boss_strength"])
            im_avatar_p2.config(file=(random_monster["boss_image"]))
        gegner_object = random_monster 
        hp_p2.config(bg='green', height=1, width=20)
        if gegner_schutz_bar > 0:
            schutz_p2.config(bg='grey', height=1, width=20)
        else:
            schutz_p2.config(bg='#d9d9d9', height=0, width=0)
        if random_monster["zustand"] == 'agressiv':
            start()
        

    def update_player_after_battle(player_file, xp_gain, money_gain):
        # Шаг 1: Загрузить данные игрока из JSON
        with open(player_file, "r", encoding="utf-8") as file:
            player = json.load(file)
        
        # Шаг 2: Добавить опыт и деньги
        player["experience"] += xp_gain
        player["money"] += money_gain
        money_gain_info = Label(root, text=f"Ты получил {money_gain} монет")
        money_gain_info.pack()
        xp_gain_info = Label(root, text=f"Ты получил {xp_gain} опыта.")
        xp_gain_info.pack()

        # Функция для удаления метки
        def delete_message():
            if money_gain_info.winfo_exists():
                money_gain_info.destroy()
            if xp_gain_info.winfo_exists():
                xp_gain_info.destroy()

        # Устанавливаем таймер на 5 секунд (5000 миллисекунд)
        root.after(5000, delete_message)

        # Шаг 3: Проверить, достиг ли игрок нового уровня
        new_level = check_level_up(player)

        # Если достиг нового уровня
        if new_level > player["level"]:
            player["level"] = new_level
            # Увеличиваем характеристики
            player["strength"] += 1
            player["endurance"] += 1
            print(f"Поздравляем! Ваш новый уровень: {new_level}")

        # Шаг 4: Сохранить изменения в JSON
        with open(player_file, "w", encoding="utf-8") as file:
            json.dump(player, file, indent=4, ensure_ascii=False)

    def check_level_up(player):
        # Определение требований к уровню
        level_requirements = {
            2: 120,
            3: 300,
            4: 550,
            5: 2500,
            6: 5000,
            7: 8250,
            8: 11350,
            9: 15350,
            10: 22000
        }

        # Проверяем текущий опыт и определяем уровень
        for level, required_xp in level_requirements.items():
            if player["experience"] < required_xp:
                return level - 1  # Возвращаем предыдущий уровень
        return 10  # Максимальный уровень

    
    # Player
    global player_health_bar, player_schutz_bar,player_attack_power, player_money, player_xp

    player_money = 0
    player_xp = 0
    player_health_bar = 0
    player_schutz_bar = 0
    player_attack_power = 0

    hp_p1 = Label(root, bg=bg_color, height=0, width=0)
    hp_p1.place(x=220, y=580)
    schutz_p1 = Label(root, bg=bg_color, height=0, width=0)
    schutz_p1.place(x=220, y=600)


    im_avatar_p1 = PhotoImage(file=(''))
    avatar_p1 = Label(root, bg="#59520e", image=im_avatar_p1)
    avatar_p1.place(x=96, y=200)


    # Gegner
    global gegner_health_bar, gegner_schutz_bar, gegner_attack_power, gegner_object
    gegner_health_bar = 0
    gegner_schutz_bar = 0
    gegner_attack_power = 0
    gegner_object = None
    
    hp_p2 = Label(root, bg=bg_color, height=0, width=0)
    hp_p2.place(x=870, y=580)
    schutz_p2 = Label(root, bg=bg_color, height=0, width=0)
    schutz_p2.place(x=870, y=600)


    im_avatar_p2 = PhotoImage(file=(''))
    avatar_p2 = Label(root, bg=bg_color, image=im_avatar_p2)
    avatar_p2.place(x=860, y=213)

    # Поле для ввода ответа
    entry = Entry(root, font=("Arial", 14))
    entry.place(x=520, y=430)

    # Отображение вопроса
    label_question = Label(root, text="", font=("Arial", 16, "bold"))
    label_question.place(x=570, y=380)

    # Кнопка "Идти дальше"
    weiter_button = Button(root, text='Идти дальше', command=gegner_suche)
    weiter_button.place(x=450, y=470)

    # Кнопка "Напасть"
    start_button = Button(root, text='Напасть', command=start, state=DISABLED)
    start_button.place(x=580, y=470)

    # Кнопка "Атаковать"
    attack_button = Button(root, text='Атаковать', command=lambda: ergebnis(gegner_health_bar, gegner_attack_power, gegner_schutz_bar, player_health_bar, player_attack_power, player_schutz_bar, gegner_object), state=DISABLED)
    attack_button.place(x=680, y=470)

    go_home_button = Button(root, text="Вернуться в главное меню", command=lambda: go_back(root, return_to_main))
    go_home_button.place(x=1100, y=60)

    root.mainloop()

def go_back(current_window, return_to_main):
    current_window.destroy()
    return_to_main()