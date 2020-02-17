from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('ZCwFUW8/2iIQd4c+TrF8FS+h+xghAwra53DJSVSZ4g9m9vSeh1kcOZDx4jTDN8qNh2WmHI5dUOEvxjNAsmdxu5Xc5GfzAlljpXblL+82K1W/cKSe3O9m35p05ezEeenZcT2YexXKH8PbOm3mfih+kwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('5a6bbbf570d855974f66395df4b0cb9e')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    respone = '轟隆隆隆🤣🤣隆隆隆隆衝衝衝衝😏😏😏拉風😎😎😎引擎發動🔑🔑🔑引擎發動+🚗+👉+🚗轟隆隆隆🤣🤣隆隆隆隆衝衝衝衝😏😏😏拉風😎😎😎引擎發動🔑🔑🔑引擎發動+🚗+👉+🚗'
    line_bot_api.reply_message(event.reply_token, respone)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
