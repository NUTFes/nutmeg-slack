import os
import requests
from slack_bolt import App
from clients.mongodb import MongoDB
from slack_bolt.adapter.flask import SlackRequestHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import datetime

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# 認証情報設定
credentials = ServiceAccountCredentials.from_json_keyfile_name('lustrous-baton-390508-40132779355a.json', scope)

# OAuth2の資格情報を使用してGoogle APIにログインする
gc = gspread.authorize(credentials)

# スプレッドシートキー(urlの"/d"と"/edit"の間の値)を[SPREADSHEET_KEY]に格納する
SPREADSHEET_KEY = os.environ.get("SPREADSHEET_KEY")
print(SPREADSHEET_KEY)

# 共有設定したGoogleSheetのsheet1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1


app = App(
  process_before_response=True,
  token=os.environ.get("SLACK_BOT_TOKEN"),
  signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

handler = SlackRequestHandler(app)

db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")
db_port = os.environ.get("DB_PORT")
db_host = os.environ.get("DB_HOST")



@app.event("app_mention")
def handle_mentions(body: dict, say):
  """ botをメンションしたときに動作する
  Args:
    body (dict): Slackのメッセージ
    say: botがメッセージするメソッド
  """
  mention = body["event"]
  user= mention["user"]
  temp_text = mention["text"]
  thread_ts = mention["ts"]

  # botのidを削除してテキスト内容のみにする
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

  # 送信者の名前をテキストで取得する
  url = "https://slack.com/api/users.list"
  response = requests.get(url, headers={"Authorization": "Bearer " + os.environ.get("SLACK_BOT_TOKEN")})
  users = response.json()["members"]
  replace_user_dict = {user["id"]:user["profile"]["display_name"] for user in users}
  sent_user_name = replace_user_dict.get(user)
  
  insert_text=[date_string, sent_user_name, text]
  print(insert_text)

  # google sheets に書き込み
  last_row_index = len(worksheet.col_values(1)) + 1
  if (insert_text in worksheet.get_all_values()) == False:
    worksheet.insert_row(insert_text, last_row_index)
    say("スプレッドシートに登録しました.\nhttps://docs.google.com/spreadsheets/d/1eu6g0o5bVSAOexjC5COzgZaqjzGSJVqrtyousFv8KCc/edit#gid=0")


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
  

if __name__ == "__main__":
  app.start(port=int(os.environ.get("PORT", 3000)))
