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
            # GOOGLE圖片蒐尋網址
            url = 'https://www.google.com/search?tbm=isch&q={}'.format(self.parameter)
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

            # 發送requests
            response = requests.get(url, headers=headers, verify=False)

            # 把爬出來的資料轉碼
            soup = BeautifulSoup(response.text, "lxml")

            # 搜詢找出所有特定的 HTML 標籤節點，這邊搜尋img的標籤，返回結果會是一個list
            items = soup.find_all("img")

            img_url = list()

            for item in items:
                # 逐一取出節點屬性
                data_iurl = item.get('data-iurl')
                # 設定正規化，必須開頭是https的字串
                avid_pattern = re.compile("^https")
                # 開始匹配，如果批配成功，會回傳1
                n = avid_pattern.match(str(data_iurl))
                if n:
                    # 批配成功，存到list中
                    img_url.append(data_iurl)
            # 隨機取一個資料出來
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