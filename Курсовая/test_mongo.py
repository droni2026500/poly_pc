import datetime
import pymongo
conn = pymongo.MongoClient(
    "mongodb://dron2026:55555@dron2026-shard-00-00-x59g6.mongodb.net:27017,dron2026-shard-00-01-x59g6.mongodb.net:27017,dron2026-shard-00-02-x59g6.mongodb.net:27017/test?ssl=true&replicaSet=dron2026-shard-0&authSource=admin&retryWrites=true&w=majority"
)
db = conn.polyclinic
coll = db.app_reception
d = datetime.datetime(2020, 11, 12, 12)
for post in coll.find({"date": {"$lt": d}}):
    print("ok")

#end = datetime.datetime.today()
#a=end.strftime(" %H:%M:%S.%f")
#print(a)
start = datetime()
print(start)