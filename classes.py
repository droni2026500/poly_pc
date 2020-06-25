from tkinter import messagebox

# Покдлючение к аккаунту БД(mongoDB),которая находится на облаке
import pymongo

conn = pymongo.MongoClient(
    "mongodb://dron2026:55555@dron2026-shard-00-00-x59g6.mongodb.net:27017,dron2026-shard-00-01-x59g6.mongodb.net:27017,dron2026-shard-00-02-x59g6.mongodb.net:27017/test?ssl=true&replicaSet=dron2026-shard-0&authSource=admin&retryWrites=true&w=majority"
)
db = conn.polyclinic
# SQLite3
import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
import platform
import datetime

time = datetime.datetime.now()
time_now = time.strftime("%d-%m-%Y %H:%M:%S")
# from registrator import *

# Класс авторизации
class Auth:
    def __init__(self, log, pas, root, main_reg):
        self.log = log
        self.pas = pas
        self.root = root
        self.main_reg = main_reg

    def log_pas(self):
        system = (
            "Система: "
            + platform.system()
            + "; Cетевое имя компьютера: "
            + platform.node()
            + "; Процессор: "
            + platform.processor()
        )
        # Присоединение к базе данных
        coll = db.registrator
        app_doc = db.app_doctor
        for login in coll.find({"login": self.log, "password": self.pas}):
            # Если все верно и специализация врача равна регистратору,то...
            if login["specialization"] == "Регистратор":
                specialization = login["specialization"]
                name = login["name"]
                params = (name, specialization, time_now, system)
                # Вставляем данные в таблицу
                cursor.execute("INSERT INTO staff_session VALUES (?,?,?,?)", params)
                # Сохраняем изменения
                conn.commit()
                self.root.destroy()  # Закрыть окно авторизации
                self.main_reg()  # Открыть окно регистратора
            else:
                # Если данные введены не правильно=ошибка
                messagebox.showinfo("ошибка", "Попопробуйте еще раз!")
            break
        else:
            for login in app_doc.find({"login": self.log, "password": self.pas}):
                if login["specialization"] == "Стоматолог-терапевт":
                    specialization = login["specialization"]
                    name = login["name"]
                    params = (name, specialization, time_now, system)
                    # Вставляем данные в таблицу
                    cursor.execute("INSERT INTO staff_session VALUES (?,?,?,?)", params)
                    # Сохраняем изменения
                    conn.commit()
                    root.destroy()  # Закрыть окно авторизации
                    terapevt()  # Открыть окно cтоматолога-терапевта
                else:
                    # Если данные введены не правильно=ошибка
                    messagebox.showinfo("ошибка", "Попопробуйте еще раз!")
            else:
                # Если данные введены не правильно=ошибка
                messagebox.showinfo("ошибка", "Попопробуйте еще раз!")


# Класс регистратора
class Registrator:
    ##    def __init__(self):
    ##

    def name_doc(self):
        coll = db.app_doctor  # Выбор коллекции из БДSSSSSSSSS
        # Поиск ФИО врача по специализации
        for spec in coll.find(
            {"specialization": "Стоматолог-терапевт"}
        ):  # Если стоматолог-терапевт
            self.ter = spec["name"]  # его ФИО
        for spec in coll.find(
            {"specialization": "Стоматолог-хирург"}
        ):  # Если стоматолог-хирург
            self.xir = spec["name"]  # его ФИО
        for spec in coll.find(
            {"specialization": "Стоматолог-ортопед"}
        ):  # Если стоматолог-ортопед
            self.ort = spec["name"]  # его ФИО
        for spec in coll.find({"specialization": "Рентгенолог"}):  # Если рентгенолог
            self.rent = spec["name"]  # его ФИО

    def raspis_ter(self):
        end = datetime.datetime.today()  # конечное время сегодня
        start = datetime.datetime.today() + datetime.timedelta(
            days=-1
        )  # начальное время сегодня(-1 день)
        coll = db.app_reception  # Подключение к коллекции
        # Цикл поиска пациентов в бд по времени и врачу(терапевт) на сегодняшний день на 9:00
        # self.kek="fasfas"
        for zap_ter_1 in coll.find(
            {"date": {"$gt": start, "$lt": end}, "doctor_id": int("1"), "time": "9:00"}
        ):
            zap_ter_1["patient_info"], zap_ter_1[
                "patient_name"
            ]  # Запись в переменные ФИО и беспокойства пациента
            self.zap_ter_11 = zap_ter_1["patient_name"]  # ФИО
            self.zap_ter_111 = zap_ter_1["patient_info"]  # Беспокойства
            btn1.place(x=450, y=35)  # Добавление кнопки если запись на это время есть
            break
        # Иначе оставляем переменные пустыми
        else:
            self.zap_ter_11 = "123"
            self.zap_ter_111 = ""
        # Цикл поиска пациентов в бд по времени и врачу(терапевт) на сегодняшний день на 10:00
        for zap_ter_2 in coll.find(
            {"date": {"$gt": start, "$lt": end}, "doctor_id": int("1"), "time": "10:00"}
        ):
            zap_ter_2["patient_info"], zap_ter_2[
                "patient_name"
            ]  # Запись в переменные ФИО и беспокойства пациента
            self.zap_ter_22 = zap_ter_2["patient_name"]  # ФИО
            self.zap_ter_222 = zap_ter_2["patient_info"]  # Беспокойства
            btn2.place(x=450, y=85)  # Добавление кнопки если запись на это время есть
            break
        # Иначе оставляем переменные пустыми
        else:
            self.zap_ter_22 = ""
            self.zap_ter_222 = ""

        # Цикл поиска пациентов в бд по времени и врачу(терапевт) на сегодняшний день на 11:00
        for zap_ter_3 in coll.find(
            {"date": {"$gt": start, "$lt": end}, "doctor_id": int("1"), "time": "11:00"}
        ):
            zap_ter_3["patient_info"], zap_ter_3[
                "patient_name"
            ]  # Запись в переменные ФИО и беспокойства пациента
            self.zap_ter_33 = zap_ter_3["patient_name"]  # ФИО
            self.zap_ter_333 = zap_ter_3["patient_info"]  # Беспокойства
            btn3.place(x=450, y=135)  # Добавление кнопки если запись на это время есть
            break
        # Иначе оставляем переменные пустыми
        else:
            self.zap_ter_33 = ""
            self.zap_ter_333 = ""

        # Цикл поиска пациентов в бд по времени и врачу(терапевт) на сегодняшний день на 12:00
        for zap_ter_4 in coll.find(
            {"date": {"$gt": start, "$lt": end}, "doctor_id": int("1"), "time": "12:00"}
        ):
            zap_ter_4["patient_info"], zap_ter_4[
                "patient_name"
            ]  # Запись в переменные ФИО и беспокойства пациента
            self.zap_ter_44 = zap_ter_4["patient_name"]  # ФИО
            self.zap_ter_444 = zap_ter_4["patient_info"]  # Беспокойства
            btn4.place(x=450, y=185)  # Добавление кнопки если запись на это время есть
            break
        # Иначе оставляем переменные пустыми
        else:
            self.zap_ter_44 = ""
            self.zap_ter_444 = ""

        # Цикл поиска пациентов в бд по времени и врачу(терапевт) на сегодняшний день на 13:00
        for zap_ter_5 in coll.find(
            {"date": {"$gt": start, "$lt": end}, "doctor_id": int("1"), "time": "13:00"}
        ):
            zap_ter_5["patient_info"], zap_ter_5[
                "patient_name"
            ]  # Запись в переменные ФИО и беспокойства пациента
            self.zap_ter_55 = zap_ter_5["patient_name"]  # ФИО
            self.zap_ter_555 = zap_ter_5["patient_info"]  # Беспокойства
            btn5.place(x=450, y=235)  # Добавление кнопки если запись на это время есть
            break
        # Иначе оставляем переменные пустыми
        else:
            self.zap_ter_55 = ""
            self.zap_ter_555 = ""
        # Цикл поиска пациентов в бд по времени и врачу(терапевт) на сегодняшний день на 14:00
        for zap_ter_6 in coll.find(
            {"date": {"$gt": start, "$lt": end}, "doctor_id": int("1"), "time": "14:00"}
        ):
            zap_ter_6["patient_info"], zap_ter_6[
                "patient_name"
            ]  # Запись в переменные ФИО и беспокойства пациента
            zap_ter_66 = zap_ter_6["patient_name"]  # ФИО
            zap_ter_666 = zap_ter_6["patient_info"]  # Беспокойства
            btn6.place(x=450, y=285)  # Добавление кнопки если запись на это время есть
            break
        # Иначе оставляем переменные пустыми
        else:
            zap_ter_66 = ""
            zap_ter_666 = ""

        # Цикл поиска пациентов в бд по времени и врачу(терапевт) на сегодняшний день на 15:00
        for zap_ter_7 in coll.find(
            {"date": {"$gt": start, "$lt": end}, "doctor_id": int("1"), "time": "15:00"}
        ):
            zap_ter_7["patient_info"], zap_ter_7[
                "patient_name"
            ]  # Запись в переменные ФИО и беспокойства пациента
            zap_ter_77 = zap_ter_7["patient_name"]  # ФИО
            zap_ter_777 = zap_ter_7["patient_info"]  # Беспокойства
            btn7.place(x=450, y=335)  # Добавление кнопки если запись на это время есть
            break
        # Иначе оставляем переменные пустыми
        else:
            zap_ter_77 = ""
            zap_ter_777 = ""
        # Цикл поиска пациентов в бд по времени и врачу(терапевт) на сегодняшний день на 16:00
        for zap_ter_8 in coll.find(
            {"date": {"$gt": start, "$lt": end}, "doctor_id": int("1"), "time": "16:00"}
        ):
            zap_ter_8["patient_info"], zap_ter_8[
                "patient_name"
            ]  # Запись в переменные ФИО и беспокойства пациента
            zap_ter_88 = zap_ter_8["patient_name"]  # ФИО
            zap_ter_888 = zap_ter_8["patient_info"]  # Беспокойства
            btn8.place(x=450, y=385)  # Добавление кнопки если запись на это время есть
            break
        # Иначе оставляем переменные пустыми
        else:
            zap_ter_88 = ""
            zap_ter_888 = ""
        # Цикл поиска пациентов в бд по времени и врачу(терапевт) на сегодняшний день на 17:00
        for zap_ter_9 in coll.find(
            {"date": {"$gt": start, "$lt": end}, "doctor_id": int("1"), "time": "17:00"}
        ):
            zap_ter_9["patient_info"], zap_ter_9[
                "patient_name"
            ]  # Запись в переменные ФИО и беспокойства пациента
            zap_ter_99 = zap_ter_9["patient_name"]  # ФИО
            zap_ter_999 = zap_ter_9["patient_info"]  # Беспокойства
            btn9.place(x=450, y=435)  # Добавление кнопки если запись на это время есть
            break
        # Иначе оставляем переменные пустыми
        else:
            zap_ter_99 = ""
            zap_ter_999 = ""
