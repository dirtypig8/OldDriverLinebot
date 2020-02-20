from PublicData.LineBotController import LineBotController
from ResultSender import ResultSender
from Module.Avgle_fn import Avgle
from Module.JavBus_fn import Javbus
from random import choice
import requests
import re
from bs4 import BeautifulSoup
from Module.LineBot import LineNotify


class Avid:
    def __init__(self, parameter, replyToken):
        self.replyToken = replyToken
        self.parameter = parameter
        self.avgle_obj = Avgle()
        self.Javbus_obj = Javbus()

    def execute(self):
        try:
            self.avgle_obj.get_avid_data(avid=self.parameter)
            self.Javbus_obj.get_avid_data(avid=self.parameter)

            message, img_url, preview_video_url = self.send_message(avid=self.parameter)

            message_list = list()
            message_list.append(ResultSender.text_send_message(text=message))
            message_list.append(ResultSender.video_send_message(original_content_url=preview_video_url,
                                                                preview_image_url=img_url))
            LineBotController.reply_message(self.replyToken, message_list)
        except Exception as e:
            message = ResultSender.text_send_message(text="找不到這部拉")
            LineBotController.reply_message(self.replyToken, message)



    def send_message(self, avid):
        title = self.avgle_obj.get_avid_information(key="title")
        embedded_key = self.avgle_obj.get_avid_information(key="embedded_url")
        if len(embedded_key[24:]) == 20:
            embedded_key = 'https://7mmtv.tv/iframe_avgle.php?code={}'.format(embedded_key[24:])
        preview_video_url = self.avgle_obj.get_avid_information(key="preview_video_url")
        keyword = self.avgle_obj.get_avid_information(key="keyword")

        img = self.Javbus_obj.get_avid_information(key='img_url')
        genre = self.Javbus_obj.get_avid_information(key='genre')
        # Seven_mm_url = self.Seven_mm.get_avid_url(avid)
        # if Seven_mm_url:
        #     Seven_mm_url = self.__build_shorten(Seven_mm_url)
        like_percent = self.avgle_obj.get_like_percent()
        duration = self.avgle_obj.get_duration()
        add_time = self.avgle_obj.get_add_time()

        message = """
番號: {} / {}
女優: {}
片名: {}
類型: {}
片長: {}分鐘
推薦指數: {}%

線上看全片
Avgle全螢幕:
{}

7mm_tv線上看:
{}
""".format(avid, add_time, keyword, title, genre, duration, like_percent, embedded_key, '暫無',
             preview_video_url)

        return message, img, preview_video_url


if __name__ == "__main__":
    Avid(parameter='JUL-110', replyToken='cf19f91ee96f43d79bb3fc362eba8be5').execute()