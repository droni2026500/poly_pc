# Библиотека tkinter
from tkinter import *
from tkinter import messagebox

# Библиотека для работы со временем
import datetime

# Библиотека для mongoDB(База данных)
import pymongo
from classes import Registrator


def main_reg():
    root1 = Tk()
    var = IntVar()  # Объявление переменной для переключаталей
    var.set(0)  # Изначально 0 = выкл
    var1 = IntVar()  # Объявление переменной для переключаталей
    var1.set(0)  # Изначально 0 = выкл
    root1.geometry("500x300")  # Размер окна
    root1.title("Окно регистратора")  # Название окна
    root1.config(background="#FFAAA8")  # Цвет фона окна
    registrator = Registrator()
    registrator.name_doc()
    # root1.resizable(width=False, height=False)#Настройка,чтобы нельзя было менять размер окна
    btn1 = Button(
        text="Перейти к расписанию", command=lambda: choose(), font="times 10"
    )  # Кнопка 'Перейти к расписанию'
    # Переключатели
    r1 = Radiobutton(
        text="Стоматолог-терапевт" + " - " + registrator.ter,
        variable=var,
        value=0,
        background="#FFAAA8",
        font="times 10",
    )
    r2 = Radiobutton(
        text="Стоматолог-хирург" + " - " + registrator.xir,
        variable=var,
        value=1,
        background="#FFAAA8",
        font="times 10",
    )
    r3 = Radiobutton(
        text="Стоматолог-ортопед" + " - " + registrator.ort,
        variable=var,
        value=2,
        background="#FFAAA8",
        font="times 10",
    )
    r4 = Radiobutton(
        text="Рентгенолог" + " - " + registrator.rent,
        variable=var,
        value=3,
        background="#FFAAA8",
        font="times 10",
    )
    r5 = Radiobutton(
        text="Сегодня" + " - " + str(datetime.date.today()),
        variable=var1,
        value=0,
        background="#FFAAA8",
        font="times 10",
    )
    btn_patient = Button(
        text="Открыть журнал пациентов", command=lambda: patient_info(), font="times 10"
    )  # Кнопка 'открыть журнал'
    # лейблы для красоты
    lbl = Label(
        text="------------------------------------------------------------------------------------------------------------",
        background="#FFAAA8",
    )
    lbl1 = Label(
        text="------------------------------------------------------------------------------------------------------------",
        background="#FFAAA8",
    )
    # Расстановка на форме
    r1.place(x=1, y=1)
    r2.place(x=1, y=25)
    r3.place(x=1, y=50)
    r4.place(x=1, y=75)
    r5.place(x=335, y=1)
    btn1.place(x=1, y=110)
    lbl.place(x=0, y=140)
    btn_patient.place(x=1, y=160)
    lbl1.place(x=0, y=185)

    # Функция для переключателей
    def choose():
        # Если стоматолог-терапевт и дата:сегодня
        if var.get() == 0 and var1.get() == 0:
            raspis_ter()  # Расписание терапевта
        # Если стоматолог-хирург и дата:сегодня
        elif var.get() == 1 and var1.get() == 0:
            rasp_xir()  # Расписание хирурга
        # Если стоматолог-ортопед и дата:сегодня
        elif var.get() == 2 and var1.get() == 0:
            rasp_ort()  # Расписание отропеда
        # Если ренгенолог и дата:сегодня
        elif var.get() == 3 and var1.get() == 0:
            rasp_rent()  # Расписание ренгенолога


# Расписание терапевта
def raspis_ter():
    rasp_ter = Tk()  # Cоздание окна
    rasp_ter.geometry("600x500")  # Размер окна
    rasp_ter.title("Расписание терапевта")  # Название окна
    rasp_ter.config(background="#FFAAA8")  # Цвет фона окна
    rasp_ter.resizable(
        width=False, height=False
    )  # Настройка,чтобы нельзя было менять размер окна
    date = Label(
        rasp_ter, text=datetime.date.today(), background="#FFAAA8", font="times 12"
    )  # Запись в лейбл сегодняшней даты

    # Кнопки с функцией
    btn1 = Button(rasp_ter, text="Пришел", command=lambda: prishel())
    btn2 = Button(rasp_ter, text="Пришел", command=lambda: prishel1())
    btn3 = Button(rasp_ter, text="Пришел", command=lambda: prishel2())
    btn4 = Button(rasp_ter, text="Пришел", command=lambda: prishel3())
    btn5 = Button(rasp_ter, text="Пришел", command=lambda: prishel4())
    btn6 = Button(rasp_ter, text="Пришел", command=lambda: prishel5())
    btn7 = Button(rasp_ter, text="Пришел", command=lambda: prishel6())
    btn8 = Button(rasp_ter, text="Пришел", command=lambda: prishel7())
    btn9 = Button(rasp_ter, text="Пришел", command=lambda: prishel8())

    end = datetime.datetime.today()  # конечное время сегодня
    start = datetime.datetime.today() + datetime.timedelta(
        days=-1
    )  # начальное время сегодня(-1 день)

    # Создание лейблов с временем
    a = Label(rasp_ter, text="9:00", background="#FFAAA8", font="times 12")
    b = Label(rasp_ter, text="10:00", background="#FFAAA8", font="times 12")
    c = Label(rasp_ter, text="11:00", background="#FFAAA8", font="times 12")
    d = Label(rasp_ter, text="12:00", background="#FFAAA8", font="times 12")
    e = Label(rasp_ter, text="13:00", background="#FFAAA8", font="times 12")
    f = Label(rasp_ter, text="14:00", background="#FFAAA8", font="times 12")
    g = Label(rasp_ter, text="15:00", background="#FFAAA8", font="times 12")
    h = Label(rasp_ter, text="16:00", background="#FFAAA8", font="times 12")
    i = Label(rasp_ter, text="17:00", background="#FFAAA8", font="times 12")

    lol = Registrator()
    lol.raspis_ter()
    print(lol.zap_ter_11)

    # Поле для вывода записи на 9:00
    a1 = Entry(rasp_ter, font=("Arial", 10, "bold"))
    a2 = Entry(rasp_ter, font=("Arial", 10, "bold"))
    a1.insert(END, lol.zap_ter_11)
    a2.insert(END, lol.zap_ter_111)
    ##    a1.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    a2.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    #Поле для вывода записи на 10;00
    ##    a3=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a4=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a3.insert(END,zap_ter_22)
    ##    a4.insert(END,zap_ter_222)
    ##    a3.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    a4.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    #Поле для вывода записи на 11:00
    ##    a5=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a6=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a5.insert(END,zap_ter_33)
    ##    a6.insert(END,zap_ter_333)
    ##    a5.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    a6.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    #Поле для вывода записи на 12:00
    ##    a7=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a8=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a7.insert(END,zap_ter_44)
    ##    a8.insert(END,zap_ter_444)
    ##    a7.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    a8.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    #Поле для вывода записи на 13:00
    ##    a9=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a10=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a9.insert(END,zap_ter_55)
    ##    a10.insert(END,zap_ter_555)
    ##    a9.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    a10.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    #Поле для вывода записи на 14:00
    ##    a11=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a12=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a11.insert(END,zap_ter_66)
    ##    a12.insert(END,zap_ter_666)
    ##    a11.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    a12.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    #Поле для вывода записи на 15:00
    ##    a13=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a14=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a13.insert(END,zap_ter_77)
    ##    a14.insert(END,zap_ter_777)
    ##    a13.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    a14.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    #Поле для вывода записи на 16:00
    ##    a15=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a16=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a15.insert(END,zap_ter_88)
    ##    a16.insert(END,zap_ter_888)
    ##    a15.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    a16.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    #Поле для вывода записи на 17:00
    ##    a17=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a18=Entry(rasp_ter,font=("Arial",10,"bold"))
    ##    a17.insert(END,zap_ter_99)
    ##    a18.insert(END,zap_ter_999)
    ##    a17.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    ##    a18.configure(disabledbackground="white",state=DISABLED,disabledforeground="black",width=50)
    btn1 = Button(
        rasp_ter, text="Обновить", command=lambda: refresh(rasp_ter)
    )  # Кнопка с функцией обновить
    # Расположение элементов в окне
    date.place(x=100, y=1)
    a.place(x=1, y=40)
    b.place(x=1, y=90)
    c.place(x=1, y=140)
    d.place(x=1, y=190)
    e.place(x=1, y=240)
    f.place(x=1, y=290)
    g.place(x=1, y=340)
    h.place(x=1, y=390)
    i.place(x=1, y=440)
    a1.place(x=80, y=30)
    a2.place(x=80, y=50)
    ##    a3.place(x=80,y=80)
    ##    a4.place(x=80,y=100)
    ##    a5.place(x=80,y=130)
    ##    a6.place(x=80,y=150)
    ##    a7.place(x=80,y=180)
    ##    a8.place(x=80,y=200)
    ##    a9.place(x=80,y=230)
    ##    a10.place(x=80,y=250)
    ##    a11.place(x=80,y=280)
    ##    a12.place(x=80,y=300)
    ##    a13.place(x=80,y=330)
    ##    a14.place(x=80,y=350)
    ##    a15.place(x=80,y=380)
    ##    a16.place(x=80,y=400)
    ##    a17.place(x=80,y=430)
    ##    a18.place(x=80,y=450)
    btn1.place(x=450, y=460)
    rasp_ter.mainloop()


# Обновление окна тервпевта
def refresh(rasp_ter):
    # Разрушение окна
    rasp_ter.destroy()
    # Запуск заново
    raspis_ter()


if __name__ == "__main__":
    main_reg()
