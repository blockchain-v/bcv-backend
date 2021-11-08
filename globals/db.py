from pymongo import MongoClient
from schemas.users import userschema

# db setup. for docker can use 'mongodb://db:27017/db'
client = MongoClient('mongodb://127.0.0.1:27017')
db = client["bcv-db"]
print(db.collection_names())
try:
    db.create_collection("users",
                         validator=userschema
                         )
except:
    print('e')