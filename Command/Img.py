from PublicData.LineBotController import LineBotController
from ResultSender import ResultSender
from random import choice
import requests
import re
from bs4 import BeautifulSoup
from Module.LineBot import LineNotify

class Img:
    def __init__(self, parameter, replyToken):
        self.replyToken = replyToken
        self.parameter = parameter

    def execute(self):
        try:
            url = 'https://www.google.com/search?tbm=isch&q={}'.format(self.parameter)
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
            response = requests.get(url, headers=headers, verify=False)  # 使用header避免訪問受到限制
            soup = BeautifulSoup(response.text, "lxml")
            # print(soup)
            items = soup.find_all("img")
            img_url=list()
            for item in items:
                data_iurl = item.get('data-iurl')
                # print(data_iurl)
                avid_pattern = re.compile("^https")
                n = avid_pattern.match(str(data_iurl))
                if n:
                    img_url.append(data_iurl)

            message_url = choice(img_url)
            # print(message_url)
            # LineNotify(access_token="VuNI0a99OAJCVtLkfC03TDozVi2HgsregB7vjLgeyQm").send(message_url)
            message = ResultSender.image_send_message(
                original_content_url=message_url, preview_image_url=message_url)
        except:
            message = ResultSender.text_send_message(text="你要找圖，你要先講!")
        # message = ResultSender.text_send_message(text=message_url)
        LineBotController.reply_message(self.replyToken, message)


if __name__ == "__main__":
    IU(parameter='', replyToken='cf19f91ee96f43d79bb3fc362eba8be5').execute()