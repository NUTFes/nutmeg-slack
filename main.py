import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(
  token=os.environ.get("SLACK_BOT_TOKEN"),
  signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("message")
def monitoring_nutfes_slack(body, logger):
  logger.info(body)
  print(body)

if __name__ == "__main__":
  app.start(port=int(os.environ.get("PORT", 3000)))
