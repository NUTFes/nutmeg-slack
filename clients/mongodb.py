from pymongo import MongoClient

# client = MongoClient("mongodb://root:password@mongo:27017")
# db = client.nutfes_slack_log
# collection_test = db.test
# collection_test.insert_one({'name': 'test2'})
# client.close()

class MongoDB:
  def __init__(self, host, port, user, password, db_name, collection_name):
    """
    コンストラクタ
    """
    self.client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
    self.db = self.client[db_name]
    self.collection = self.db[collection_name]

  def insert(self, data):
      self.collection.insert_one(data)

  def close(self):
    self.client.close()

