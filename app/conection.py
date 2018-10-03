import pymongo
cliente = pymongo.MongoClient("mongodb://localhost:27017/analysis_data")
p = cliente.analysis_data.violence_events.find()
for i in p:
	print i
# /*mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
# myquery = { "address": "Park Lane 38" }
# mydoc = mycol.find(myquery)