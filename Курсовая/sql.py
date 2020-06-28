import sqlite3
#conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
#cursor = conn.cursor()

# Создание таблицы
#cursor.execute("""CREATE TABLE price
 #                 (doctor_id, doctor, officium)
 #              """)

conn = sqlite3.connect("mydatabase.db")
# conn.row_factory = sqlite3.Row
cursor = conn.cursor()

sql = "SELECT * FROM price WHERE doctor_id=?"
cursor.execute(sql, [("2")])
a=cursor.fetchall()
print(a)# or use fetchone()