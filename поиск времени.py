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

array_doc=[]
coll=db.app_doctor
for doc in coll.find({}):
    array_doc.append(doc["id"])
print(array_doc[0])


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

##array_zapis_fio=[]
##array_zapis_worry=[]
##a=0
##b=0
##while a<len(array_doc):
##    while b<len(array_time):
##        for zap_ter_1 in coll.find({"date":{"$gt":start,"$lt":end},"doctor_id":array_doc[a],"time":array_time[b]}):
##            array_zapis_fio.append(zap_ter_1["patient_name"])#ФИО
##            array_zapis_worry.append(zap_ter_1["patient_info"])#Беспокойства
##        b+=1
##    a+=1
##
##print("fio"+str(array_zapis_fio))
##print("worry"+str(array_zapis_worry))









