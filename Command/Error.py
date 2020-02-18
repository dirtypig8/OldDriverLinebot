from PublicData.LineBotController import LineBotController
from ResultSender import ResultSender

class NotFoundCommand:
    def __init__(self, replyToken):
        self.replyToken = replyToken
    def execute(self):
        message = ResultSender.text_send_message(text="感謝您的幫忙")
        LineBotController.line_bot_api(self.replyToken, message)
        print(self.replyToken)