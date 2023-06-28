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
