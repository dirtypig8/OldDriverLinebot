from PublicData.LineBotController import LineBotController
from ResultSender import ResultSender
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from random import choice
import requests
import re
from bs4 import BeautifulSoup


class Fuzzy:
    def __init__(self, parameter, replyToken):
        self.replyToken = replyToken
        self.parameter = parameter

    def execute(self):
        message_list = list()
        try:
            target_license_plate = self.parameter[0]

            del self.parameter[0]
            license_plate_list = self.parameter

            result_list = process.extract(query=target_license_plate, choices=license_plate_list)

            message = '{} -> {}'.format(target_license_plate, result_list)
            print(message)
            message_list.append(ResultSender.text_send_message(text=message))
            LineBotController.reply_message(self.replyToken, message_list)

        except Exception as e:
            error_message = '比對失敗 : {}'.format(e)
            message_list.append(ResultSender.text_send_message(text=error_message))
            LineBotController.reply_message(self.replyToken, message_list)

if __name__ == "__main__":
    Fuzzy(parameter=['abc1111', '1111' , '1133'], replyToken='cf19f91ee96f43d79bb3fc362eba8be5').execute()