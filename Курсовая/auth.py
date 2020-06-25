from tkinter import *
import pymongo
import sqlite3
import platform
import datetime
from tkinter import messagebox


class Connect_MongoDB:
    def __init__(self, conn):
        self.mongo_connector = pymongo.MongoClient(
                conn)
    def connect_database(self, db):
        self.db_connector = getattr(self.mongo_connector, db)
    def connect_coll(self, coll):
        self.coll_connector = getattr(self.db_connector, coll)

connections = Connect_MongoDB(
    "mongodb://dron2026:55555@dron2026-shard-00-00-x59g6.mongodb.net:27017,dron2026-shard-00-01-x59g6.mongodb.net:27017,dron2026-shard-00-02-x59g6.mongodb.net:27017/test?ssl=true&replicaSet=dron2026-shard-0&authSource=admin&retryWrites=true&w=majority")
connections.connect_database('polyclinic')
connections.connect_coll('registrator')
abr = connections.coll_connector
for login in abr.find({"login": "dron", "password": "1234"}):
    print("ok")


class Connect_SQLite:
    def __init__(self, conn_sql):
        self.conn_sql = sqlite3.connect(conn_sql)
        self.cursor = self.conn_sql.cursor()
        self.commit = self.conn_sql.commit()

#connection_SQL = Connect_SQLite("mydatabase.db")
#params = ("1", "1", "1", "1")
#connection_SQL.cursor.execute("INSERT INTO staff_session VALUES (?,?,?,?)", params)
#connection_SQL.commit


class Auth_registrator(Connect_MongoDB, Connect_SQLite ):
    def __init__(self, login, passwords):
        self.login = login
        self.passwords = passwords
    def system_har(self):
        self.time = datetime.datetime.now()
        self.time_now = self.time.strftime("%d-%m-%Y %H:%M:%S")
        self.system = (
                "Система: "
                + platform.system()
                + "; Cетевое имя компьютера: "
                + platform.node()
                + "; Процессор: "
                + platform.processor()
        )
    def log_pas_registrator(self):
        connection_SQL = Connect_SQLite("mydatabase.db")
        connections = Connect_MongoDB(
            "mongodb://dron2026:55555@dron2026-shard-00-00-x59g6.mongodb.net:27017,dron2026-shard-00-01-x59g6.mongodb.net:27017,dron2026-shard-00-02-x59g6.mongodb.net:27017/test?ssl=true&replicaSet=dron2026-shard-0&authSource=admin&retryWrites=true&w=majority")
        connections.connect_database('polyclinic')
        connections.connect_coll('registrator')
        for log in connections.coll_connector.find({"login": login, "password": passwordsы}):
            # Если все верно и специализация врача равна регистратору,то...
            if log["specialization"] == "Регистратор":
                specialization = login["specialization"]
                name = login["name"]
                params = (name, specialization, self.time_now, self.system)
                # Вставляем данные в таблицу
                connection_SQL.cursor.execute("INSERT INTO staff_session VALUES (?,?,?,?)", params)
                connection_SQL.commit
            else:
                # Если данные введены не правильно=ошибка
                messagebox.showinfo("ошибка", "Попопробуйте еще раз!")
            break





def main():
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
        command=lambda: Auth_registrator.log_pas_registrator(enter_login.get(), enter_password.get()),
        # lambda: log(enter_login, enter_password, root, main_reg)
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


if __name__ == "__main__":
    main()
