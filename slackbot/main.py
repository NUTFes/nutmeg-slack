import os
import requests
from slack_bolt import App
from clients.mongodb import MongoDB
from slack_bolt.adapter.flask import SlackRequestHandler
import gspread

from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# 認証情報設定
credentials = ServiceAccountCredentials.from_json_keyfile_name('lustrous-baton-390508-40132779355a.json', scope)

# OAuth2の資格情報を使用してGoogle APIにログインする
gc = gspread.authorize(credentials)

# スプレッドシートキー(urlの"/d"と"/edit"の間の値)を[SPREADSHEET_KEY]に格納する
SPREADSHEET_KEY = '1eu6g0o5bVSAOexjC5COzgZaqjzGSJVqrtyousFv8KCc'

# 共有設定したGoogleSheetのsheet1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

import_value = int(worksheet.acell('A1').value)

export_value = import_value+100
worksheet.update_cell(1, 2, export_value)


app = App(
  process_before_response=True,
  token=os.environ.get("SLACK_BOT_TOKEN"),
  signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# ngrok を使っている場合 http://localhost:4040/inspect/http でも確認できますが
# リスナーのログと同時に見るためにペイロードを標準出力に表示するだけの middleware です

handler = SlackRequestHandler(app)

db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")
db_port = os.environ.get("DB_PORT")
db_host = os.environ.get("DB_HOST")

@app.event("app_mention")
def handle_mentions(say):

  say(
    blocks=blocks_input_form()
  )

@app.action("button-submit-aciton")
def handle_button_submit(ack: Ack, body: dict, ):
  ack()
  say("ぼたんが押されました")
  print(body)


@app.event("message")
def monitoring_nutfes_slack(body: dict):
  """ Slackのメッセージを監視する
  Args:
    body (dict): Slackのメッセージ
  """
  mongo = MongoDB(db_host, db_port, db_user , db_password, db_name, "log")
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

  mongo = MongoDB(db_host, db_port, db_user , db_password, db_name, "channel")
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

  mongo = MongoDB(db_host, db_port, db_user , db_password, db_name,"user")
  registered_user_dict = mongo.find()
  if registered_user_dict == None:
    mongo.insert(replace_user_dict)
  mongo.update(registered_user_dict, replace_user_dict)

def blocks_input_form():
  return [
        {
      "type": "section",
      "text": {
        "type": "plain_text",
        "text": "以下の3つを入力してください",
        "emoji": True
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "input",
      "element": {
        "type": "plain_text_input",
        "multiline": True,
        "action_id": "plain_text_input-action"
      },
      "label": {
        "type": "plain_text",
        "text": "内容の詳細",
        "emoji": True
      }
    },
    {
      "type": "input",
      "element": {
        "type": "plain_text_input",
        "action_id": "plain_text_input-action"
      },
      "label": {
        "type": "plain_text",
        "text": "氏名",
        "emoji": True
      }
    },
    {
      "type": "input",
      "element": {
        "type": "datepicker",
        "initial_date": "2023-06-01",
        "placeholder": {
          "type": "plain_text",
          "text": "Select a date",
          "emoji": True
        },
        "action_id": "datepicker-action"
      },
      "label": {
        "type": "plain_text",
        "text": "日付",
        "emoji": True
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "最後に，右の\"登録\"ボタンを押してください．"
      },
      "accessory": {
        "type": "button",
        "text": {
          "type": "plain_text",
          "text": "登録",
          "emoji": True
        },
        "style": "primary",
        "value": "click_me_123",
        "action_id": "button-submit-aciton"
      }
    }

  ]

if __name__ == "__main__":
  app.start(port=int(os.environ.get("PORT", 3000)))
