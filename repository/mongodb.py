from pymongo import MongoClient

client = MongoClient("mongodb://root:password@mongo:27017")
db = client.nutfes_slack_log
collection_test = db.test
collection_test.insert_one({'name': 'test2'})
client.close()
