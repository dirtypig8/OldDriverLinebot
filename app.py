from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from Module.LineBot import LineNotify
from InteractiveServer import CommandExecutor
from PublicData.LineBotController import LineBotController
from ResultSender import ResultSender
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('ZCwFUW8/2iIQd4c+TrF8FS+h+xghAwra53DJSVSZ4g9m9vSeh1kcOZDx4jTDN8qNh2WmHI5dUOEvxjNAsmdxu5Xc5GfzAlljpXblL+82K1W/cKSe3O9m35p05ezEeenZcT2YexXKH8PbOm3mfih+kwdB04t89/1O/w1cDnyilFU=')
LineBotController.line_bot_api = line_bot_api
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
    # message = TextSendMessage(text=event.message.text)
    # re = "你輸入的是: '{}'\n\n感謝您的幫忙".format(event.message.text)
    # preview_video_url = 'https://static-clst.avgle.com/videos/tmb11/370977/preview.mp4'
    # img_url = 'https://pics.javbus.com/cover/7hot_b.jpg'
    # message = VideoSendMessage(original_content_url=preview_video_url, preview_image_url=img_url)
    # message = TextSendMessage(text=re)
    # message = ImageSendMessage(original_content_url='https://i.imgur.com/Hn6lBtg.jpg',preview_image_url='https://i.imgur.com/Hn6lBtg.jpg')
    # line_bot_api.reply_message(event.reply_token, message)

    try:
        profile = line_bot_api.get_profile(user_id=event.source.user_id)
        profile_information = "\n使用者: {}\n照片URL: {}".format(profile.display_name, profile.picture_url)
        line_notify_message = "\n{}\n\nmessage: '{}'".format(profile_information, event)
        LineNotify(access_token="VuNI0a99OAJCVtLkfC03TDozVi2HgsregB7vjLgeyQm").send(line_notify_message)

        CommandExecutor().execute(command_json=event)



    except Exception as e:
        error_message = 'handle_message: {}'.format(e)
        LineNotify(access_token="VuNI0a99OAJCVtLkfC03TDozVi2HgsregB7vjLgeyQm").send(error_message)
import os
if __name__ == "__main__":
    LineBotController.reply_message = line_bot_api.reply_message
    ResultSender.text_send_message = TextSendMessage
    ResultSender.image_send_message = ImageSendMessage
    ResultSender.video_send_message = VideoSendMessage
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
