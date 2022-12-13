from flask import Flask

# def main():
#   payload = {
#     "channel": os.environ["SLACKBOT_CHANNEL_ID"],
#   }
#   headers = {
#     "Authorization": "Bearer " + os.environ["TOKEN"]
#   }
#   response = requests.get(os.environ["SLACK_URL"], params=payload, headers=headers).json()
#   with open("message.json", "w", encoding="utf-8") as f:
#     json.dump(response, f, ensure_ascii=False)

app = Flask(__name__)
@app.route("/")
def index():
  return "Hello World!"

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=3000)

