import os
from pymongo import MongoClient, collection
client = MongoClient("mongodb+srv://ammar:ammar1122@kent.7ewag.mongodb.net/kent?retryWrites=true&w=majority")
db = client.cluster["kent"]
collection=db["jsondata"]

obj=db.collection.find("{Nat-m.:green}")