import os
from pymongo import MongoClient

# client = MongoClient("mongodb://root:password@mongo:27017")
# db = client.nutfes_slack_log
# collection_test = db.test
# collection_test.insert_one({'name': 'test2'})
# client.close()

class MongoDB:
  def __init__(self, host, port, user, password, db_name, collection_name):
    """ コンストラクタ
    Args:
      host (str): ホスト名
      port (int): ポート番号
      user (str): ユーザー名
      password (str): パスワード
      db_name (str): DB名
      collection_name (str): コレクション名
    """
    self.client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
    self.db = self.client[db_name]
    self.collection = self.db[collection_name]

  def insert(self, log):
    """ DBにデータを挿入する
      Args:
        log (dict): 挿入するメッセージログ
    """
    self.collection.insert_one(log)

