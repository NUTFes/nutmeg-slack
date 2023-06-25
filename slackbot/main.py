import os
import requests
from slack_bolt import App, Ack, BoltResponse, BoltContext, Respond, Say
from clients.mongodb import MongoDB
from slack_bolt.adapter.flask import SlackRequestHandler
import gspread
import logging
from logging import Logger
from typing import Callable, Dict, List
from oauth2client.service_account import ServiceAccountCredentials
from slack_sdk import WebClient
import re
import datetime

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# 認証情報設定
credentials = ServiceAccountCredentials.from_json_keyfile_name('lustrous-baton-390508-40132779355a.json', scope)

# OAuth2の資格情報を使用してGoogle APIにログインする
gc = gspread.authorize(credentials)

# スプレッドシートキー(urlの"/d"と"/edit"の間の値)を[SPREADSHEET_KEY]に格納する
SPREADSHEET_KEY = '1eu6g0o5bVSAOexjC5COzgZaqjzGSJVqrtyousFv8KCc'

# 共有設定したGoogleSheetのsheet1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

# import_value = int(worksheet.acell('A1').value)

# export_value = import_value+100
# worksheet.update_cell(1, 2, export_value)


app = App(
  process_before_response=True,
  token=os.environ.get("SLACK_BOT_TOKEN"),
  signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# ngrok を使っている場合 http://localhost:4040/inspect/http でも確認できますが
# リスナーのログと同時に見るためにペイロードを標準出力に表示するだけの middleware です
@app.use
def log_request(logger: Logger, body : dict, next: Callable[[], BoltResponse]):
  logger.info(body)
  next()

handler = SlackRequestHandler(app)

db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")
db_port = os.environ.get("DB_PORT")
db_host = os.environ.get("DB_HOST")

@app.event("app_mention")
def handle_mentions(ack, context, body, say, logger, request):
  mention = body["event"]
  user= mention["user"]
  temp_text = mention["text"]
  channel = mention["channel"]
  thread_ts = mention["ts"]

  # botのidを削除してテキスト内容飲みにする
  text = re.sub(r'\<.*?\>', '', temp_text)

  # Unix時刻を秒とマイクロ秒に分割
  seconds = int(float(thread_ts))
  microseconds = int((float(thread_ts) - seconds) * 1000000)

  # Unixエポック時間を日付に変換
  date = datetime.datetime.fromtimestamp(seconds) + datetime.timedelta(hours=9)

  # マイクロ秒を追加
  date_with_microseconds = date + datetime.timedelta(microseconds=microseconds)

  # 日付を文字列に変換
  date_string = date_with_microseconds.strftime('%Y/%m/%d %H:%M:%S')
  print(date_string)

  url = "https://slack.com/api/users.list"
  response = requests.get(url, headers={"Authorization": "Bearer " + os.environ.get("SLACK_BOT_TOKEN")})
  users = response.json()["members"]
  replace_user_dict = {user["id"]:user["profile"]["display_name"] for user in users}
  # print(replace_user_dict)
  sent_user_name = replace_user_dict.get(user)
  print(replace_user_dict.get(user))
   

  insert_text=[date_string, sent_user_name, text]


  print(f"メンションされました:{text}")
  
  # google sheets に書き込み
  last_row_index = len(worksheet.col_values(1)) + 1
  if not insert_text in worksheet.get_all_values():
    worksheet.insert_row(insert_text, last_row_index)
    # say(','.join(insert_text))
    say("スプレッドシートに登録しました.\nhttps://docs.google.com/spreadsheets/d/1eu6g0o5bVSAOexjC5COzgZaqjzGSJVqrtyousFv8KCc/edit#gid=0")
  
  print(last_row_index, insert_text)
  
  
  # say(
  #   blocks=blocks_input_form()
  # )


# @app.command("/register-googlesheet")
# def handle_register_slashcommand(ack: Ack, body: dict, client: WebClient):
#   ack()
#   client.views_open(
#     trigger_id=body["trigger_id"],
#     view=build_modal_view(),
#   )


# @app.view("modal-id")
# def handle_view_events(ack: Ack, view: dict, logger: logging.Logger):
#   inputs = view["state"]["values"]

#   question = input.get("question-block", {}).get("plain_text_input-action", {}).get("value")

#   logger.info(f"モーダルを受け付けました\n 内容は: {question}")
#   ack()
  


# @app.action("button-submit-aciton")
# def handle_button_submit(ack: Ack, body: dict, say: Say):
#   ack()
#   say("ぼたんが押されました")
#   print(body.user.id)

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
  



def build_modal_view():
  return {
    "type": "modal",
    "callback_id": "modal-id",
    "title": {
      "type": "plain_text",
      "text": "スプレッドシート登録モーダル",
      "emoji": True
    },
    "submit": {
      "type": "plain_text",
      "text": "Submit",
      "emoji": True
    },
    "close": {
      "type": "plain_text",
      "text": "Cancel",
      "emoji": True
    },
    "blocks": [
      {
        "type": "input",
        "block_id": "question-block",
        "element": {
          "type": "plain_text_input",
          "multiline": True,
          "action_id": "plain_text_input-action"
        },
        "label": {
          "type": "plain_text",
          "text": "スプレッドシートに登録する内容を入力してください．",
          "emoji": True
        }
      }
    ]
  }



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
        "action_id": "plain_text_input-action-1"
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
        "action_id": "plain_text_input-action-2"
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
