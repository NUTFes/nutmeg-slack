import requests
import os
import json

def main():
  payload = {
    "channel": os.environ["SLACKBOT_CHANNEL_ID"],
  }
  headers = {
    "Authorization": "Bearer " + os.environ["TOKEN"]
  }
  response = requests.get(os.environ["SLACK_URL"], params=payload, headers=headers).json()
  with open("message.json", "w", encoding="utf-8") as f:
    json.dump(response, f, ensure_ascii=False)

if __name__ == "__main__":
  main()

