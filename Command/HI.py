from PublicData.LineBotController import LineBotController
from ResultSender import ResultSender
from random import choice
import requests
import re
from bs4 import BeautifulSoup

class HI:
    def __init__(self, parameter, replyToken):
        self.replyToken = replyToken
        self.parameter = parameter

    def execute(self):
        message = ResultSender.text_send_message(text="HIHI 你好")
        LineBotController.reply_message(self.replyToken, message)


if __name__ == "__main__":
    IU(parameter='', replyToken='cf19f91ee96f43d79bb3fc362eba8be5').execute()