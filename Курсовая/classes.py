from tkinter import messagebox
from tkinter import *
import pymongo
import sqlite3
import platform
import datetime

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
connections.connect_coll("registrator")
abr = connections.coll_connector
for login in abr.find({"login": "dron", "password": "1234"}):
    pass


class Connect_SQLite:
    def __init__(self, conn_sql):
        self.conn_sql = sqlite3.connect(conn_sql)
        self.cursor = self.conn_sql.cursor()
        self.commit = self.conn_sql.commit


# connection_SQL = Connect_SQLite("mydatabase.db")
# params = ("1", "1", "1", "1")
# connection_SQL.cursor.execute("INSERT INTO staff_session VALUES (?,?,?,?)", params)
# connection_SQL.commit()
# print(connection_SQL.commit)


class Auth(Connect_MongoDB, Connect_SQLite):
    def __init__(self, log, pas):
        self.log = log
        self.pas = pas

    def log_pas(self):
        connection_SQL = Connect_SQLite("mydatabase.db")
        connections = Connect_MongoDB(
            "mongodb://dron2026:55555@dron2026-shard-00-00-x59g6.mongodb.net:27017,dron2026-shard-00-01-x59g6.mongodb.net:27017,dron2026-shard-00-02-x59g6.mongodb.net:27017/test?ssl=true&replicaSet=dron2026-shard-0&authSource=admin&retryWrites=true&w=majority"
        )
        connections.connect_database("polyclinic")
        connections.connect_coll("registrator")
        for log in connections.coll_connector.find(
            {"login": self.log, "password": self.pas}
        ):
            # Если все верно и специализация врача равна регистратору,то...
            if log["specialization"] == "Регистратор":
                specialization = login["specialization"]
                name = login["name"]
                params = (name, specialization, time_now, system)
                # Вставляем данные в таблицу
                connection_SQL.cursor.execute(
                    "INSERT INTO staff_session VALUES (?,?,?,?)", params
                )
                connection_SQL.commit()
                root.destroy()
                main_reg()
            else:
                # Если данные введены не правильно=ошибка
                messagebox.showinfo("ошибка", "Попопробуйте еще раз!")
            break
        else:
            for log in connections.coll_connector.find(
                {"login": self.log, "password": self.pas}
            ):
                if log["specialization"] == "Стоматолог-терапевт":
                    specialization = login["specialization"]
                    name = login["name"]
                    params = (name, specialization, time_now, system)
                    # Вставляем данные в таблицу
                    connection_SQL.cursor.execute(
                        "INSERT INTO staff_session VALUES (?,?,?,?)", params
                    )
                    connection_SQL.commit()
                    root.destroy()
                else:
                    # Если данные введены не правильно=ошибка
                    messagebox.showinfo("ошибка", "Попопробуйте еще раз!")
            else:
                # Если данные введены не правильно=ошибка
                messagebox.showinfo("ошибка", "Попопробуйте еще раз!")


class Registrator:
    def __init__(self):
        pass

    @staticmethod
    def choose():
        global doctor, id_, array_zapis_fio, array_zapis_worry, array_time
        id_ = -1
        doctor = -1
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
                connections = Connect_MongoDB(
                    "mongodb://dron2026:55555@dron2026-shard-00-00-x59g6.mongodb.net:27017,dron2026-shard-00-01-x59g6.mongodb.net:27017,dron2026-shard-00-02-x59g6.mongodb.net:27017/test?ssl=true&replicaSet=dron2026-shard-0&authSource=admin&retryWrites=true&w=majority"
                )
                connections.connect_database("polyclinic")
                connections.connect_coll("app_reception")
                iii = 0
                ccc = 0
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
            elif var.get() == 0:
                messagebox.showinfo("Ошибка", "Выберите врача!")
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
        raspis_doc()

    @staticmethod
    def raspis_doc_window():
        i = 0
        entr_place = 0
        lbl_place = 0
        worry_place = 0
        if len(array_zapis_fio) == 0:
            print("yaya")
            label_dont = Label(
                doctor_main, text="Записей нет!", background="#FFAAA8", font="times 12",
            )
            label_dont.place(x=300, y=250)
        else:
            while i < len(array_zapis_fio):
                time1 = Label(
                    doctor_main,
                    text=array_time[i],
                    background="#FFAAA8",
                    font="times 12",
                )
                time1.place(x=1, y=40 + lbl_place)
                lbl_name = Entry(doctor_main, font=("Arial", 10, "bold"))
                lbl_name.insert(END, array_zapis_fio[i])
                lbl_name.place(x=80, y=40 + entr_place)
                lbl_worry = Entry(doctor_main, font=("Arial", 10, "bold"))
                lbl_worry.insert(END, array_zapis_worry[i])
                lbl_worry.place(x=80, y=60 + worry_place)
                btn_prishel = Button(text="Пришел", command="")
                btn_prishel.place(x=)
                worry_place += 50
                entr_place += 50
                lbl_place += 50
                i += 1

    @staticmethod
    def main_reg_window():
        global array_doc_id, array_doc
        connections = Connect_MongoDB(
            "mongodb://dron2026:55555@dron2026-shard-00-00-x59g6.mongodb.net:27017,dron2026-shard-00-01-x59g6.mongodb.net:27017,dron2026-shard-00-02-x59g6.mongodb.net:27017/test?ssl=true&replicaSet=dron2026-shard-0&authSource=admin&retryWrites=true&w=majority"
        )
        connections.connect_database("polyclinic")
        connections.connect_coll("app_doctor")
        btn1 = Button(
            text="Перейти к расписанию", command=lambda: choose_class(), font="times 10"
        )  # Кнопка 'Перейти к расписанию'
        i = 0
        radio_place = 0
        btn_place = 0
        vari = 0
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
                array_var.append(var.get())
                i += 1
                radio_place += 24
                btn_place += 5


def raspis_doc():
    global doctor_main
    time_now_doc = time.strftime("%d-%m-%Y")
    doctor_main = Tk()
    doctor_main.geometry("600x500")  # Размер окна
    doctor_main.title("Расписание " + str(array_doc[doctor]))  # Название окна
    doctor_main.config(background="#FFAAA8")  # Цвет фона окна
    doctor_main.resizable(
        width=False, height=False
    )  # Настройка,чтобы нельзя было менять размер окна
    date = Label(
        doctor_main, text=time_now_doc, background="#FFAAA8", font="times 12"
    )  # Запись в лейбл сегодняшней даты
    window_main = Registrator()
    window_main.raspis_doc_window()
    # print(array_time)
    print("fio" + str(array_zapis_fio))
    print("worry" + str(array_zapis_worry))
    date.place(x=100, y=1)
    doctor_main.mainloop()


def main_reg():
    global var, root1
    root1 = Tk()
    var = IntVar()  # Объявление переменной для переключаталей
    var.set(0)  # Изначально 0 = выкл
    root1.geometry("500x300")  # Размер окна
    root1.title("Окно регистратора")  # Название окна
    root1.config(background="#FFAAA8")  # Цвет фона окна
    var = IntVar()  # Объявление переменной для переключаталей
    var.set(0)  # Изначально 0 = выкл
    window_main_reg = Registrator()
    window_main_reg.main_reg_window()
    root1.mainloop()


def choose_class():
    ch_class = Registrator()
    ch_class.choose()
    print(ch_class)

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
        command=lambda: authorization(),
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


def authorization():
    auth = Auth(enter_login.get(), enter_password.get())
    auth.log_pas()


if __name__ == "__main__":
    main()
