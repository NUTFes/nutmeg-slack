import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pymongo import MongoClient
from clients.mongodb import MongoDB

app = App(
  token=os.environ.get("SLACK_BOT_TOKEN"),
  signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("message")
def monitoring_nutfes_slack(body, logger):
  mongo = MongoDB("mongo", 27017, "root", "password", "nutfes_slack_log", "log")
  mongo.insert(body)
  logger.info(body)
  print(body)

if __name__ == "__main__":
  app.start(port=int(os.environ.get("PORT", 3000)))
