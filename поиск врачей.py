from tkinter import messagebox
#Покдлючение к аккаунту БД(mongoDB),которая находится на облаке
import pymongo
conn = pymongo.MongoClient("mongodb://dron2026:55555@dron2026-shard-00-00-x59g6.mongodb.net:27017,dron2026-shard-00-01-x59g6.mongodb.net:27017,dron2026-shard-00-02-x59g6.mongodb.net:27017/test?ssl=true&replicaSet=dron2026-shard-0&authSource=admin&retryWrites=true&w=majority")
db=conn.polyclinic
#SQLite3
import sqlite3
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
import platform
import datetime
#Библиотека tkinter
from tkinter import *
from tkinter import messagebox
#Библиотека для работы со временем
import datetime
#Библиотека для mongoDB(База данных)
import pymongo
#Импорт классов

def main_reg():
    coll=db.app_doctor
    root1=Tk()
    var=IntVar()#Объявление переменной для переключаталей
    var.set(0)#Изначально 0 = выкл
    root1.geometry("500x300")#Размер окна
    root1.title("Окно регистратора")#Название окна
    root1.config(background="#FFAAA8")#Цвет фона окна
    var=IntVar()#Объявление переменной для переключаталей
    var.set(0)#Изначально 0 = выкл
    btn1=Button(text="Перейти к расписанию",command=lambda:choose(array_doc),font="times 10")#Кнопка 'Перейти к расписанию'
    #Переменные
    i=0
    radio_place=0
    btn_place=0
    vari=0
    #Массивы
    array_doc_id=[]
    array_doc=[]
    array_var=[]
    for doc in coll.find({}):
        array_doc.append(doc["specialization"])
        array_doc_id.append(doc["id"])
        while i<len(array_doc):
            radio=Radiobutton(text=array_doc[i],variable=var,value=1+i,background="#FFAAA8",font="times 10")
##            print(array_doc_id[i]==var.get())
            radio.place(x=1,y=1+radio_place)
            btn1.place(x=1,y=110+btn_place)
            array_var.append(var.get())
            i+=1
            radio_place+=24
            btn_place+=5
            
            
    
##    print(array_var)
##    print(array_doc_id)
    def choose(array_doc):
        global doctor
        id_=-1
        doctor=-1
        while id_<(len(array_doc_id)):
            id_+=1
            doctor+=1
            if var.get() == array_doc_id[id_]:
                array_doc[doctor]
                raspis_doc(array_doc)
                break
            elif var.get()==0:
                messagebox.showinfo("Ошибка","Выберите врача!")
                break
                

    
def raspis_doc(array_doc):
    doc=Tk()
    doc.geometry("600x500")#Размер окна
    doc.title("Расписание " + str(array_doc[doctor]))#Название окна
    doc.config(background="#FFAAA8")#Цвет фона окна
    doc.resizable(width=False, height=False)#Настройка,чтобы нельзя было менять размер окна
    time=datetime.datetime.now()
    time_now=(time.strftime("%d-%m-%Y"))
    date=Label(doc,text=time_now,background="#FFAAA8",font="times 12")#Запись в лейбл сегодняшней даты


    date.place(x=100,y=1)
    doc.mainloop()

    def lable_time():
        None
        

#Поиск времени
def time_search():
    array_zapis_fio=[]
    array_zapis_worry=[]
    array_time=[]                
    end = datetime.datetime.today()#конечное время сегодня
    start=datetime.datetime.today()+ datetime.timedelta(days=-1)#начальное время сегодня(-1 день)
    coll=db.app_reception#Подключение к коллекции
    i=0
    c=0
    while i<len(array_doc):
        for time in coll.find({"date":{"$gt":start,"$lt":end},"doctor_id":array_doc[i]}):
            array_time.append(time["time"])
            while c<len(array_time):
                for zapis in coll.find({"date":{"$gt":start,"$lt":end},"doctor_id":array_doc[i],"time":array_time[c]}):
                    if array_doc[i] == 1:
                        #zapis_ter_name=zapis["patient_name"]
                        #zapis_ter_worry=zapis["patient_info"]

                        array_zapis_fio.append(zapis["patient_name"])#ФИО
                        array_zapis_worry.append(zapis["patient_info"])#Беспокойства
                    elif array_doc[i] == 2:
                        print("2")
                    elif array_doc[i] == 3:
                        print("3")
                    elif array_doc[i] == 4:
                        print("4")
                        
                c+=1
        i+=1
    print(array_time)
    print("fio"+str(array_zapis_fio))
    print("worry"+str(array_zapis_worry))









if __name__ == '__main__':
    main_reg()



