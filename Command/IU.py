from PublicData.LineBotController import LineBotController
from ResultSender import ResultSender

class IU:
    def __init__(self, parameter, replyToken):
        self.replyToken = replyToken
        self.parameter = parameter
    def execute(self):
        message = ResultSender.text_send_message(text="你才咪妃，你全家都咪妃!")
        LineBotController.reply_message(self.replyToken, message)