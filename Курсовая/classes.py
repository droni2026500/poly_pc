from tkinter import messagebox
from tkinter import *
import pymongo
import sqlite3
import platform
import datetime

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk


from tkcalendar import Calendar, DateEntry


time = datetime.datetime.now()
time_now = time.strftime("%d-%m-%Y %H:%M:%S")
system = (
    "Система: "
    + platform.system()
    + "; Cетевое имя компьютера: "
    + platform.node()
    + "; Процессор: "
    + platform.processor()
)


class Connect_MongoDB:
    def __init__(self, conn):
        self.mongo_connector = pymongo.MongoClient(conn)

    def connect_database(self, db):
        self.db_connector = getattr(self.mongo_connector, db)

    def connect_coll(self, coll):
        self.coll_connector = getattr(self.db_connector, coll)


connections = Connect_MongoDB(
    "mongodb://dron2026:55555@dron2026-shard-00-00-x59g6.mongodb.net:27017,dron2026-shard-00-01-x59g6.mongodb.net:27017,dron2026-shard-00-02-x59g6.mongodb.net:27017/test?ssl=true&replicaSet=dron2026-shard-0&authSource=admin&retryWrites=true&w=majority"
)
connections.connect_database("polyclinic")


class Connect_SQLite:
    def __init__(self, conn_sql):
        self.conn_sql = sqlite3.connect(conn_sql)
        self.cursor = self.conn_sql.cursor
        self.commit = self.conn_sql.commit


connection_SQL = Connect_SQLite("mydatabase.db")
cursor = connection_SQL.cursor()


class Auth(Connect_MongoDB, Connect_SQLite):
    def __init__(self, log, pas):
        self.log = log
        self.pas = pas

    @staticmethod
    def main():
        global enter_login, enter_password, root
        # Окно авторизации
        root = Tk()  # Создание окна
        root.geometry("300x250")  # Размер окна
        root.title("Войти в систему")  # Название окна
        root.config(background="#fff44f")  # Фон формы
        root.resizable(
            width=False, height=False
        )  # Настройка,чтобы нельзя было изменять размер окна
        text_log = Label(
            text="Вход в систему", background="#fff44f", font="times 12"
        )  # Лейбл 'ход в систему'
        text_enter_login = Label(
            text="Введите ваш логин:", background="#fff44f", font="times 12"
        )  # Лейбл введите логин
        enter_login = Entry()  # Поле ввода логина
        text_enter_pass = Label(
            text="Введите ваш пароль:", background="#fff44f", font="times 12"
        )  # Лейбл "Введите ваш пароль"
        enter_password = Entry(show="*")  # Поле ввода пароля
        button_enter = Button(
            text="Войти",
            command=lambda: Auth(
                enter_login.get(), enter_password.get()
            ).log_pas_registrator(),
            background="#71bc78",
            foreground="white",
            font="times 12",
        )  # Кнопка входа
        # Расположение элементов на форме
        text_log.pack()
        text_enter_login.pack()
        enter_login.pack()
        text_enter_pass.pack()
        enter_password.pack()
        button_enter.pack()
        root.mainloop()

    def log_pas_registrator(self):
        global specialization, name, id_docs
        connections.connect_coll("registrator")
        for log in connections.coll_connector.find(
            {"login": self.log, "password": self.pas}
        ):
            # Если все верно и специализация врача равна регистратору,то...
            if log["specialization"] == "Регистратор":
                specialization = log["specialization"]
                name = log["name"]
                params = (name, specialization, time_now, system)
                # Вставляем данные в таблицу
                cursor.execute("INSERT INTO staff_session VALUES (?,?,?,?)", params)
                connection_SQL.commit()
                root.destroy()
                Registrator.main_reg()
            else:
                # Если данные введены не правильно=ошибка
                messagebox.showinfo("ошибка", "Попопробуйте еще раз!")
            break
        else:
            self.log = "droni2026500"
            self.pas = "124"
            connections.connect_coll("app_doctor")
            for log in connections.coll_connector.find(
                {"login": self.log, "password": self.pas}
            ):
                print("ok")
                specialization = log["specialization"]
                name = log["name"]
                id_docs = log["id"]
                params = (name, specialization, time_now, system)
                # Вставляем данные в таблицу
                cursor.execute("INSERT INTO staff_session VALUES (?,?,?,?)", params)
                connection_SQL.commit()
                root.destroy()
                Doctors.doctors_main()
                break
            else:
                messagebox.showinfo("ошибка", "Попопробуйте еще раз!")


class Registrator:
    def __init__(self):
        pass

    @staticmethod
    def main_reg():
        global var, root1
        root1 = Tk()
        root1.geometry("700x400")  # Размер окна
        root1.title("Окно регистратора")  # Название окна
        root1.config(background="#FFAAA8")  # Цвет фона окна
        var = IntVar()  # Объявление переменной для переключаталей
        var.set(0)  # Изначально 0 = выкл
        window_main_reg = Registrator()
        window_main_reg.main_reg_window()
        root1.mainloop()

    @staticmethod
    def choose():
        global doctor, id_, array_zapis_fio, array_zapis_worry, array_time
        id_ = -1
        doctor = -1
        if var.get() == 0:
            messagebox.showinfo("Ошибка", "Выберите врача!")
        else:
            while id_ < (len(array_doc_id)):
                id_ += 1
                doctor += 1
                if var.get() == array_doc_id[id_]:
                    array_doc[doctor]
                    array_zapis_fio = []
                    array_zapis_worry = []
                    array_time = []
                    end = datetime.datetime.today()  # конечное время сегодня
                    start = datetime.datetime.today() + datetime.timedelta(
                        days=-1
                    )  # начальное время сегодня(-1 день)
                    # print(start)
                    connections.connect_coll("app_reception")
                    iii = 0
                    while iii < len(array_doc[doctor]):
                        for time_poisk in connections.coll_connector.find(
                            {
                                "date": {"$gt": start, "$lt": end},
                                "doctor_id": array_doc_id[id_],
                            }
                        ):
                            array_time.append(time_poisk["time"])
                            # array_time.sort(key = lambda date: datetime.strptime(date, '%H'))
                        iii += 1
                        break
                    break
            print(array_time)
            array_time.sort()
            print(array_time)
            ccc = 0
            while ccc < len(array_time):
                for zapis in connections.coll_connector.find(
                    {
                        "date": {"$gt": start, "$lt": end},
                        "doctor_id": array_doc_id[id_],
                        "time": array_time[ccc],
                    }
                ):
                    array_zapis_fio.append(zapis["patient_name"])  # ФИО
                    array_zapis_worry.append(zapis["patient_info"])  # Беспокойства
                ccc += 1
            Registrator.raspis_doc()

    @staticmethod
    def raspis_doc_window():
        i = 0
        entr_place = 0
        lbl_place = 0
        worry_place = 0
        if len(array_zapis_fio) == 0:
            label_dont = Label(
                doctor_main, text="Записей нет!", background="#FFAAA8", font="times 14",
            )
            label_dont.place(x=250, y=250)
        else:
            while i < len(array_zapis_fio):
                time1 = Label(
                    doctor_main,
                    text=array_time[i],
                    background="#FFAAA8",
                    font="times 14",
                )
                time1.place(x=1, y=40 + lbl_place)
                lbl_name = Entry(doctor_main, font="times 14")
                lbl_name.insert(END, array_zapis_fio[i])
                lbl_name.place(x=80, y=40 + entr_place)
                lbl_worry = Entry(doctor_main, font="times 14")
                lbl_worry.insert(END, array_zapis_worry[i])
                lbl_worry.place(x=80, y=60 + worry_place)
                worry_place += 50
                entr_place += 50
                lbl_place += 50
                i += 1

    @staticmethod
    def main_reg_window():
        global array_doc_id, array_doc
        connections.connect_coll("app_doctor")
        btn1 = Button(
            text="Перейти к расписанию",
            command=lambda: Registrator.choose(),
            font="times 12",
        )  # Кнопка 'Перейти к расписанию'
        lbl_1 = Label(
            text="------------------------------------------------------------------------------------------------------------",
            background="#FFAAA8",
            font="times 14",
        )
        lbl_2 = Label(
            text="------------------------------------------------------------------------------------------------------------",
            background="#FFAAA8",
            font="times 14",
        )
        btn2 = Button(
            text="Редактирование услуг врача",
            command=lambda: Registrator.edit_price(),
            font="times 12",
        )
        btn3 = Button(
            text="Журнал пациентов",
            command=lambda: Registrator.patient_journal(),
            font="times 12",
        )
        btn4 = Button(
            text="Выбор даты",
            command=lambda: Registrator.date_entry_main(),
            font="times 12",
        )
        btn5 = Button(
            text="Отчет посещений за день",
            command=lambda: Registrator.date_entry_main(),
            font="times 12",
        )
        btn6 = Button(
            text="Отчет заработка за период",
            command=lambda: Registrator.date_entry_main(),
            font="times 12",
        )
        i = 0
        radio_place = 0
        btn_place = 0
        # Массивы
        array_doc_id = []
        array_doc = []
        array_var = []
        for doc in connections.coll_connector.find({}):
            array_doc.append(doc["specialization"])
            array_doc_id.append(doc["id"])
            while i < len(array_doc):
                radio = Radiobutton(
                    text=array_doc[i] + "(" + doc["name"] + ")",
                    variable=var,
                    value=1 + i,
                    background="#FFAAA8",
                    font="times 10",
                )
                radio.place(x=1, y=1 + radio_place)
                btn1.place(x=1, y=110 + btn_place)
                lbl_1.place(x=1, y=135 + btn_place)
                lbl_2.place(x=1, y=180 + btn_place)
                btn2.place(x=1, y=155 + btn_place)
                btn3.place(x=1, y=200 + btn_place)
                btn4.place(x=350, y=10)
                btn5.place(x=1, y=250 + btn_place)
                btn6.place(x=1, y=300 + btn_place)
                array_var.append(var.get())
                i += 1
                radio_place += 24
                btn_place += 10

    @staticmethod
    def date_entry_main():
        first_date = ""

        def print_sel():
            global first_date
            first_date = str(cal.selection_get())
            print(first_date)
            root.destroy()

        root = Tk()
        root.title("Выбор даты")
        a = datetime.date.today().year
        b = datetime.date.today().month
        c = datetime.date.today().day

        cal = Calendar(
            root,
            font="Arial 14",
            selectmode="day",
            locale="Ru",
            cursor="hand1",
            year=a,
            month=b,
            day=c,
        )

        cal.pack(fill="both", expand=True)
        Button(root, text="ok", command=print_sel).pack()

    @staticmethod
    def raspis_doc():
        global doctor_main
        time_now_doc = time.strftime("%d-%m-%Y")
        doctor_main = Tk()
        doctor_main.geometry("600x500")  # Размер окна
        doctor_main.title(
            "Расписание " + (str(array_doc[doctor]).lower())
        )  # Название окна
        doctor_main.config(background="#FFAAA8")  # Цвет фона окна
        doctor_main.resizable(
            width=False, height=False
        )  # Настройка,чтобы нельзя было менять размер окна
        date = Label(
            doctor_main, text=time_now_doc, background="#FFAAA8", font="times 12"
        )  # Запись в лейбл сегодняшней даты
        window_main = Registrator()
        window_main.raspis_doc_window()
        print("fio" + str(array_zapis_fio))
        print("worry" + str(array_zapis_worry))
        date.place(x=100, y=1)
        doctor_main.mainloop()

    @staticmethod
    def main_edit_price():
        global price_main
        price_main = Tk()
        price_main.geometry("800x900")  # Размер окна
        price_main.title(
            "Редактирование услуг " + (str(array_doc[doctor_]).lower())
        )  # Название окна
        price_main.config(background="#FFAAA8")  # Цвет фона окна
        price_main.resizable(
            width=False, height=False
        )  # Настройка,чтобы нельзя было менять размер окна
        lbl_nomen = Label(
            price_main, text="Наиминование", background="#FFAAA8", font="times 12"
        )
        lbl_nomen.place(x=100, y=1)
        lbl_price = Label(
            price_main, text="Цена", background="#FFAAA8", font="times 12"
        )
        lbl_price.place(x=390, y=1)
        btn_add = Button(
            price_main,
            text="Добавить услугу",
            command=lambda: Registrator.add_nomen(),
            font="times 12",
        )
        btn_add.place(x=250, y=250)
        btn_save = Button(
            price_main,
            text="Сохранить",
            command=lambda: Registrator.save_price(),
            font="times 12",
        )
        btn_save.place(x=400, y=400)
        Registrator.edit_price_fucnk()
        # lbl_number=Label(text="1"+i)

        price_main.mainloop()

    @staticmethod
    def edit_price():
        global doctor_, id__
        id__ = -1
        doctor_ = -1
        if var.get() == 0:
            messagebox.showinfo("Ошибка", "Выберите врача!")
        else:
            while id__ < (len(array_doc_id)):
                id__ += 1
                doctor_ += 1
                if var.get() == array_doc_id[id__]:
                    array_doc[doctor_]
                    print(str(array_doc_id[id__]))
                    Registrator.main_edit_price()

    @staticmethod
    def edit_price_fucnk():
        price_i = 0
        lbl_number_i = 1
        sql = "SELECT officium FROM price WHERE doctor_id=?"
        cursor.execute(sql, [(str(array_doc_id[id__]))])
        abc = cursor.fetchall()
        sql1 = "SELECT price FROM price WHERE doctor_id=?"
        cursor.execute(sql1, [(str(array_doc_id[id__]))])
        abc1 = cursor.fetchall()
        lbl_number_place = 0
        while price_i < len(abc):
            lbl_number = Label(
                price_main,
                text=str(lbl_number_i),
                font="times 12",
                background="#FFAAA8",
            )
            lbl_number.place(x=1, y=25 + lbl_number_place)
            entry_nomen = Entry(price_main)
            entry_nomen.insert(END, abc[price_i])
            entry_nomen.place(x=100, y=25 + lbl_number_place)
            entry_price = Entry(price_main)
            entry_price.insert(END, abc1[price_i])
            entry_price.place(x=350, y=25 + lbl_number_place)
            btn_delete = Button(
                price_main,
                text="Удалить",
                command=lambda: Registrator.delete_price(),
                font="times 11",
            )
            btn_delete.place(x=550, y=21 + lbl_number_place)
            lbl_number_i += 1
            lbl_number_place += 35
            print("1")
            price_i += 1

    @staticmethod
    def delete_price():
        pass

    @staticmethod
    def save_price():
        pass

    @staticmethod
    def add_nomen():
        params = ("1", "safasf", "рубашка", "300р")
        # Вставляем данные в таблицу
        cursor.execute("INSERT INTO price VALUES (?,?,?,?)", params)
        connection_SQL.commit()
        print("ok")

    @staticmethod
    def patient_journal():
        global polis_entr, text_journal
        root_info = Tk()  # Создание окна
        root_info.geometry("825x600")  # Размер окна
        root_info.title("Журал пациентов")  # Название окна
        root_info.config(background="#FFAAA8")  # Цвет фона окна
        root_info.resizable(
            width=False, height=False
        )  # Настройка,чтобы нельзя было менять размер окна
        lbl_polis = Label(
            root_info, text="Введите номер полиса (16 цифр)", background="#FFAAA8"
        )  # Лейбл
        polis_entr = Entry(root_info, width=40)  # Поле ввода полиса
        btn_polis = Button(
            root_info,
            text="Найти",
            command=lambda: Registrator.patient_journal_funk(),
            background="#FFAAA8",
        )  # Кнопка поиска пациентов по полису
        text_journal = Text(
            root_info, width=100, height=30, wrap=WORD
        )  # Текстовой поле для вывода информации
        btn_delete = Button(
            root_info,
            text="Очистить",
            command=lambda: Registrator.patient_journal_clear(),
            background="#FFAAA8",
        )  # Кнопка для оичстки текстового поля
        # Расстановка элементов на форме
        lbl_polis.place(x=20, y=5)
        polis_entr.place(x=1, y=40)
        btn_polis.place(x=1, y=60)
        btn_delete.place(x=50, y=60)
        text_journal.place(x=1, y=90)
        root_info.mainloop()

    @staticmethod
    def patient_journal_funk():
        connections.connect_coll("patient")
        pol = polis_entr.get()  # Запись в переменную текста из поля ввода
        # Поиск совпадения в БД по введенном полису
        for pat_inf in connections.connect_coll.find({"polis": pol}):
            # Запись в переменную
            info = (
                "Имя врача:"
                + pat_inf["doc_name"]
                + " ,"
                + "Cпециализация:"
                + pat_inf["doc_spec"]
                + " ,"
                + "ФИО пацента:"
                + pat_inf["patient_name"]
                + " ,"
                + "Информация о пациенте:"
                + pat_inf["patient_info"]
                + " ,"
                + "Дата посещения:"
                + str(pat_inf["date"])
                + " ,"
                + "Время посещения:"
                + pat_inf["time"]
                + " ,"
                + "Полис:"
                + pat_inf["polis"]
                + " ,"
                + "Услуги:"
                + pat_inf["service"]
                + " ,"
                + "Комментарий врача:"
                + pat_inf["comment"]
                + "\n"
                + "---------------------------------------------------------------------------------------------------"
                + "\n"
            )
            text_journal.insert(1.0, info)  # Вывод информации в текстовое поле

    @staticmethod
    def patient_journal_clear():
        polis_entr.delete(0, END)
        text_journal.delete(1.0, END)  # Очистить поле


class Doctors(Registrator, Auth):
    def __init__(self):
        pass

    @staticmethod
    def doctors_main():
        global doctor_main_window
        time_now_doc = time.strftime("%d-%m-%Y")
        doctor_main_window = Tk()
        doctor_main_window.geometry("1000x800")  # Размер окна
        doctor_main_window.title("Расписание " + (specialization))  # Название окна
        doctor_main_window.config(background="#FFAAA8")  # Цвет фона окна
        doctor_main_window.resizable(
            width=False, height=False
        )  # Настройка,чтобы нельзя было менять размер окна
        date = Label(
            doctor_main_window, text=time_now_doc, background="#FFAAA8", font="times 12"
        )  # Запись в лейбл сегодняшней даты
        name_label = Label(
            doctor_main_window,
            text="Врач: " + name,
            background="#FFAAA8",
            font="times 12",
        )
        lbl_fio_pat = Label(
            doctor_main_window,
            text="ФИО пациента",
            background="#FFAAA8",
            font="times 12",
        )
        lbl_worry_pat = Label(
            doctor_main_window,
            text="Беспокойства",
            background="#FFAAA8",
            font="times 12",
        )
        lbl_fio_pat.place(x=100, y=20)
        lbl_worry_pat.place(x=400, y=20)
        Doctors.saffsa()
        Doctors.doctors_main_functions()
        date.place(x=10, y=1)
        name_label.place(x=1, y=780)
        doctor_main_window.mainloop()

    @staticmethod
    def doctors_main_functions():
        i = 0
        entr_place = 0
        lp=""
        if len(array_zapis_fio_doc) == 0:
            label_dont = Label(
                doctor_main_window,
                text="Записей нет!",
                background="#FFAAA8",
                font="times 14",
            )
            label_dont.place(x=250, y=250)
        else:

            while i < len(array_zapis_fio_doc):
                time1 = Label(
                    doctor_main_window,
                    text=sortedArray[i],
                    background="#FFAAA8",
                    font="times 14",
                )
                time1.place(x=1, y=60 + entr_place)
                lbl_name = Entry(doctor_main_window, font="times 12")
                lbl_name.insert(END, array_zapis_fio_doc[i]["patient_name"])
                lbl_name.configure(
                    disabledbackground="white",
                    state=DISABLED,
                    disabledforeground="black",
                    width=30,
                )
                lbl_name.place(x=80, y=60 + entr_place)
                lbl_worry = Entry(doctor_main_window, font="times 12")
                lbl_worry.insert(END, array_zapis_worry_doc[i])
                lbl_worry.configure(
                    disabledbackground="white",
                    state=DISABLED,
                    disabledforeground="black",
                    width=35,
                )
                lbl_worry.place(x=350, y=60 + entr_place)
                btn_info_pat = Button(
                    doctor_main_window,
                    text="Карточка пациента",
                    command=lambda: Doctors.patient_card(),
                )
                lp = array_zapis_fio_doc[i]["id"]
                btn_spend = Button(
                    doctor_main_window,
                    text="Выбор услуги",
                    command=lambda lp=lp: Doctors.spend(lp),
                )
                btn_info_pat.place(x=650, y=60 + entr_place)
                btn_spend.place(x=800, y=60 + entr_place)
                entr_place += 50
                i += 1

    @staticmethod
    def saffsa():
        global array_zapis_fio_doc, array_zapis_worry_doc, array_time_doc, array_polis, array_id_patient, sortedArray
        array_time_doc = []
        array_zapis_fio_doc = []
        array_zapis_worry_doc = []
        array_polis = []
        array_id_patient = []
        end = datetime.datetime.today()  # конечное время сегодня
        start = datetime.datetime.today() + datetime.timedelta(
            days=-1
        )  # начальное время сегодня(-1 день)
        # print(start)
        connections.connect_coll("app_reception")
        for poisk_time in connections.coll_connector.find(
            {"date": {"$gt": start, "$lt": end}, "doctor_id": id_docs}
        ):
            array_time_doc.append(poisk_time["time"])
            array_polis.append(poisk_time["polis"])
            print(array_polis)
        print(array_time_doc)
        sortedArray = sorted(
            array_time_doc,
            key=lambda x: datetime.datetime.strptime(x, '%H:%M')
        )
        print(sortedArray)
        ccc = 0
        while ccc < len(sortedArray):
            for zapis in connections.coll_connector.find(
                {
                    "date": {"$gt": start, "$lt": end},
                    "doctor_id": id_docs,
                    "time": sortedArray[ccc],
                }
            ):
                array_id_patient.append(zapis["id"])
                array_zapis_fio_doc.append(zapis)
                print(array_zapis_fio_doc)
                # print(array_zapis_fio_doc)# ФИО
                array_zapis_worry_doc.append(zapis["patient_info"])  # Беспокойства
            ccc += 1

    @staticmethod
    def patient_card():
        patient_card_main = Tk()  # Создание окна
        patient_card_main.geometry("825x600")  # Размер окна
        patient_card_main.title("Журал пациентов")  # Название окна
        patient_card_main.config(background="#FFAAA8")  # Цвет фона окна
        patient_card_main.resizable(
            width=False, height=False
        )  # Настройка,чтобы нельзя было менять размер окна
        lbl_polis = Label(
            patient_card_main,
            text="Введите номер полиса (16 цифр)",
            background="#FFAAA8",
        )  # Лейбл
        polis_entr = Entry(patient_card_main, width=40)  # Поле ввода полиса
        btn_polis = Button(
            patient_card_main,
            text="Найти",
            command=lambda: Registrator.patient_journal_funk(),
            background="#FFAAA8",
        )  # Кнопка поиска пациентов по полису
        text_journal = Text(
            patient_card_main, width=100, height=30, wrap=WORD
        )  # Текстовой поле для вывода информации
        btn_delete = Button(
            patient_card_main,
            text="Очистить",
            command=lambda: Registrator.patient_journal_clear(),
            background="#FFAAA8",
        )  # Кнопка для оичстки текстового поля
        # Расстановка элементов на форме
        lbl_polis.place(x=20, y=5)
        polis_entr.place(x=1, y=40)
        btn_polis.place(x=1, y=60)
        btn_delete.place(x=50, y=60)
        text_journal.place(x=1, y=90)
        patient_card_main.mainloop()

    @staticmethod
    def spend(id_button):
        global list_cb, abc, array_provesti, search_patient
        array_provesti = []
        doctor_main_window.destroy()
        spend_main_window = Tk()
        spend_main_window.geometry("825x600")  # Размер окна
        spend_main_window.title("Записи услуг")  # Название окна
        spend_main_window.config(background="#FFAAA8")  # Цвет фона окна
        spend_main_window.resizable(
            width=False, height=False
        )  # Настройка,чтобы нельзя было менять размер окна
        cvar1 = BooleanVar(value=0)
        pr = 0
        connections.connect_coll("app_reception")
        print(id_button)
        for search_patient in connections.coll_connector.find({"id": id_button}):
            search_patient
            sql = "SELECT officium,price FROM price WHERE doctor_id=?"
            cursor.execute(sql, [(str(search_patient["doctor_id"]))])
            abc = cursor.fetchall()
        plus = 0
        list_cb = []
        kek = ""
        for pr in range(len(abc)):
            list_cb.append(IntVar())
            list_cb[-1].set(0)
            c1 = Checkbutton(
                text=abc[pr],
                variable=list_cb[-1],
                background="#FFAAA8",
                font="times 12",
                command=lambda pr=pr: Doctors.provesti_pat(pr),
                onvalue=1,
                offvalue=0
            )
            c1.place(x=1,y=30+plus)
            plus += 30
        btn_ok = Button(spend_main_window, text="Провести", command=lambda: Doctors.spend_trans(),font="times 14")
        btn_ok.place(x=1,y=140+plus)
        lbl_com = Label(spend_main_window,text="Комметарий:", background="#FFAAA8", font="times 14")
        lbl_com.place(x=1,y=60+plus)
        entry_com = Entry(spend_main_window)
        entry_com.place(x=1, y=100 + plus)
        lbl_price_nomen = Label(spend_main_window, text="Выбор услуги:", background="#FFAAA8", font="times 14")
        lbl_price_nomen.place(x=1, y=1)
        lbl_patient_name = Label(spend_main_window, text="Пациент:"+search_patient["patient_name"], background="#FFAAA8", font="times 14")
        lbl_patient_name.place(x=1, y=570)
        spend_main_window.mainloop()

    @staticmethod
    def provesti_pat(pr):
        global array_provesti
        if list_cb[pr].get() == 1:
            array_provesti.append(abc[pr])
        else:
            array_provesti.remove(abc[pr])
    @staticmethod
    def spend_trans():
        connections.connect_coll("patient")
        print(search_patient["patient_name"])
        patient_info = {"doctor_id": search_patient["doctor_id"], "patient_name": search_patient["patient_name"],
                         "patient_info": search_patient["patient_info"],
                        "date": search_patient["date"], "time": search_patient["time"],
                         "polis": search_patient["polis"], "service": array_provesti, "comment": "sddasdas",
                         "doc_name": name, "doc_spec": specialization}
        connections.connect_coll.insert_one(patient_info)
        print(array_provesti)

if __name__ == "__main__":
    # Registrator.main_reg()
    Auth.main()
