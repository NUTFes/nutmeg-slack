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

def register_channel_name():
  """ Slackのチャンネル名を{id:name}として登録する
  """
  url = "https://slack.com/api/conversations.list"
  response = requests.get(url, headers={"Authorization": "Bearer " + os.environ.get("SLACK_BOT_TOKEN")})
  channels = response.json()["channels"]
  replace_channel_dict = {channel["id"]:channel["name"] for channel in channels}

  mongo = MongoDB("mongo", 27017, "root", "password", os.environ.get("DB"), "channel")
  registered_channel_dict = mongo.find()
  mongo.update(registered_channel_dict ,replace_channel_dict)

if __name__ == "__main__":
  app.start(port=int(os.environ.get("PORT", 3000)))
