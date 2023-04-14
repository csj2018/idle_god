import requests, re

class Danmu():
    def __init__(self):
        self.baseurl = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
        # 要获取的弹幕的直播间号
        self.roomid = 11826642
        # 请求头
        self.headers = {
            'Host': 'api.live.bilibili.com',
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
        }
        # 传递的参数
        self.data = {
            'roomid': self.roomid,
            'csrf_token': '',
            'csrf': '',
            'visit_id': '',
        }
        self.rndl = []
        self.cmd = []

    def getdanmu(self, first_time = 0):
        self.req = requests.post(url=self.baseurl, headers=self.headers, data=self.data)
        self.html = self.req.json()
        self.code = self.html['code']
        if self.req.status_code == 200 and self.code == 0:
            for dic in self.html['data']['room']:
                rnd = dic['rnd']
                if rnd not in self.rndl:
                    self.rndl.append(rnd)
                    text = dic['text']
                    if "#" in text and first_time != 1:
                        self.cmd.append(re.split('#', text)[-1])
        while len(self.rndl) > 10:
            self.rndl.pop(0)