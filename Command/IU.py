from PublicData.LineBotController import LineBotController
from ResultSender import ResultSender
from random import choice
import requests
import re
from bs4 import BeautifulSoup

class IU:
    def __init__(self, parameter, replyToken):
        self.replyToken = replyToken
        self.parameter = parameter

    def execute(self):
        url = 'https://www.google.com.sg/search?q={}&tbm=isch&tbs=sbd:0'.\
            format("IU")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)  # 使用header避免訪問受到限制
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('img')
        img_url=list()
        for item in items:
            url = item.get('src')
            # print(url)
            avid_pattern = re.compile("^http")
            n = avid_pattern.match(str(url))
            if n:
                img_url.append(url)

        message_url = choice(img_url)
        print(message_url)
        message = ResultSender.image_send_message(
            original_content_url=message_url, preview_image_url=message_url)
        # message = ResultSender.text_send_message(text="你才咪妃，你全家都咪妃!")
        LineBotController.reply_message(self.replyToken, message)


if __name__ == "__main__":
    IU(parameter='', replyToken='cf19f91ee96f43d79bb3fc362eba8be5').execute()