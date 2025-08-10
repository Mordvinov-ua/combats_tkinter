from tkinter import *
import random

def battle_window(return_to_main):
    root = Tk()

    root.geometry("1400x700")

    atacka = IntVar()
    atacka.set(0)
    blockk = IntVar() 
    blockk.set(0)
    def choise():
        x = random.choice((1,2,3))
        return x
        
    def start():
        if atacka.get() != choise() and atacka.get() != 0:
            if hp_p2['width'] == 2:
                hp_p2['bg'] = 'red'
                hp_p2['width'] -= 2
                avatar_p2['image'] = smert
            hp_p2['width'] -= 2 
        if blockk.get() != choise() and blockk.get() != 0:
            if hp_p1['width'] == 2:
                hp_p1['bg'] = 'red'
                hp_p1['width'] -= 2
                avatar_p1['image'] = smert
                
            hp_p1['width'] -= 2 

        blockk.set(0)
        atacka.set(0)
        



    # HP
    hp_p1 = Label(root, bg= 'green', height=1, width=20)
    hp_p1.place(x=40, y=20)

    hp_p2 = Label(root, bg= 'green', height=1, width=20)
    hp_p2.place(x=500, y=20)

    # Avatar
    smert = PhotoImage(file='combats_tkinter/images/krest.png')

    im_avatar_p1 = PhotoImage(file=('combats_tkinter/images/knight.png'))
    avatar_p1 = Label(root, image=im_avatar_p1)
    avatar_p1.place(x=40, y=60)

    im_avatar_p2 = PhotoImage(file=('combats_tkinter/images/monstr.png'))
    avatar_p2 = Label(root, image=im_avatar_p2)
    avatar_p2.place(x=480, y=60)

    # Boi
    Atack_head = Radiobutton(root, text='атака в голову', variable=atacka, value=1)
    Atack_head.place(x=200, y=100)
    Atack_body = Radiobutton(root, text='атака в тело', variable=atacka, value=2)
    Atack_body.place(x=200, y=150)
    Atack_leg = Radiobutton(root, text='атака в ноги', variable=atacka, value=3)
    Atack_leg.place(x=200, y=200)

    Block_head = Radiobutton(root, text='блок головы', variable=blockk, value=1)
    Block_head.place(x=350, y=100)
    Block_body = Radiobutton(root, text='блок корпуса', variable=blockk, value=2)
    Block_body.place(x=350, y=150)
    Block_leg = Radiobutton(root, text='блок ног', variable=blockk, value=3)
    Block_leg.place(x=350, y=200)

    start_button = Button(root, text='Атака', command=start)
    start_button.place(x=300, y=300)

    Button(root, text="Вернуться в главное меню", command=lambda: go_back(root, return_to_main)).pack()

    root.mainloop()

def go_back(current_window, return_to_main):
    current_window.destroy()
    return_to_main()