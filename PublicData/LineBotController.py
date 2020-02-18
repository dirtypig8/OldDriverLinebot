class LineBotController:
    line_bot_api=None


    @staticmethod
    def send_text_message(reply_token, message):
        message = LineBotController.TextSendMessage(text=message)
        LineBotController.reply_message(reply_token, message)