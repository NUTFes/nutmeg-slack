import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pymongo import MongoClient
from clients.mongodb import MongoDB

app = App(
  token=os.environ.get("SLACK_BOT_TOKEN"),
  signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("message")
def monitoring_nutfes_slack(body: dict):
  """ Slackのメッセージを監視する
  Args:
    body (dict): Slackのメッセージ
  """
  mongo = MongoDB("mongo", 27017, "root", "password", os.environ.get("DB"), "log")
  mongo.insert(body)
  register_channel_name()
  register_user_name()

def register_channel_name():
  """ Slackのチャンネル名を{id:name}として登録する
  """
  url = "https://slack.com/api/conversations.list"
  response = requests.get(url, headers={"Authorization": "Bearer " + os.environ.get("SLACK_BOT_TOKEN")})
  channels = response.json()["channels"]
  replace_channel_dict = {channel["id"]:channel["name"] for channel in channels}

  mongo = MongoDB("mongo", 27017, "root", "password", os.environ.get("DB"), "channel")
  registered_channel_dict = mongo.find()
  if registered_channel_dict == None:
    mongo.insert(replace_channel_dict)
  mongo.update(registered_channel_dict, replace_channel_dict)


def register_user_name():
  """ Slackのユーザ名を{id:name}として登録する
  """
  url = "https://slack.com/api/users.list"
  response = requests.get(url, headers={"Authorization": "Bearer " + os.environ.get("SLACK_BOT_TOKEN")})
  users = response.json()["members"]
  replace_user_dict = {user["id"]:user["profile"]["display_name"] for user in users}

  mongo = MongoDB("mongo", 27017, "root", "password", os.environ.get("DB"), "user")
  registered_user_dict = mongo.find()
  if registered_user_dict == None:
    mongo.insert(replace_user_dict)
  mongo.update(registered_user_dict, replace_user_dict)

if __name__ == "__main__":
  app.start(port=int(os.environ.get("PORT", 3000)))
