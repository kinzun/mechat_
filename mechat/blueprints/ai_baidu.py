import os
import subprocess
import json
import requests

from aip import AipSpeech, AipNlp
from uuid import uuid4

BASE_PATH = os.path.dirname(__file__)
FILE_STORAGE = os.path.join(os.path.dirname(__file__), 'file_storage')
MP3TO = os.path.join(FILE_STORAGE, 'auido.mp3')
K16PCM = os.path.join(FILE_STORAGE, '16k.pcm')

postdata = {
    "reqType": 0,
    "perception": {
        "inputText": {
            "text": "天气"
        },
        # "inputImage": {
        #     "url": "imageUrl"
        # },
        "selfInfo": {
            "location": {
                "city": "北京",
                "province": "北京",
                "street": "王府井"
            }
        }
    },
    "userInfo": {
        # "apiKey": "4379f116c989477ca34ba64e27096c6c",
        "apiKey": "d7d27f73930f4df5bcc8bbfcb2b73e3f",
        "userId": "test"
    }
}


class Baidu_AI(object):
    """ 你的 APPID AK SK """

    def __init__(self):
        self.APP_ID = '15837841'
        self.API_KEY = 'YGFhrAvDpsDVpGUr3NZr5nE8'
        self.SECRET_KEY = 'bI8nk7jopdhLPY2mqR14uoefMmotWRBi'
        self._client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def speech_synthesis(self, text_messages):
        ''' 语音合成'''
        result = self._client.synthesis(text_messages, 'zh', 1, {
            'vol': 5,  # 0 -15 音量
            'per': 4,  # 0-4 人声 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
            'spd': 5,  # 0- 15 语速
            'pit': 5,  # 0 -15 音调
        })

        fileuuid = f'{uuid4()}' + ".mp3"

        # fileuuid_ = os.path.join(FILE_STORAGE, fileuuid)

        if not isinstance(result, dict):
            # with open(MP3TO, 'wb') as f:
            #     f.write(result)
            with open(os.path.join(FILE_STORAGE,fileuuid), 'wb') as f:
                f.write(result)
        return fileuuid

    def speech_recognition(self, mp3name, tofile=K16PCM):
        '''语音识别'''

        def get_file_content(filePath):
            with open(filePath, 'rb') as fp:
                return fp.read()

            # 识别本地文件

        try:
            if not os.path.isfile(K16PCM):
                completed = subprocess.run(
                    f'docker run -v={FILE_STORAGE}:/tmp/ffmpeg opencoconut/ffmpeg  -y -i {mp3name}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm',
                    shell=True, )
        except Exception as e:
            print(e)
        else:
            print(completed.returncode)

        # else:
        #     self._client.asr(get_file_content(K16PCM), 'pcm', 16000, {
        #         'dev_pid': 1536,
        #     })
        try:
            res = self._client.asr(get_file_content(tofile), 'pcm', 16000, {
                'dev_pid': 1536,
            })

        except:
            pass

        if res.get('err_msg') == 'success.':
            os.remove(K16PCM)
            return res.get('result')[0]
        else:

            print(res)

    def natural_language(self, text_):
        nlp_ai = AipNlp(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        res = nlp_ai.simnet(text_, "你叫什么")
        if res.get('score') >= 0.90:
            print(res.get('score'))
            return '我是你爸爸'

        if nlp_ai.simnet(text_, '你多大了').get('score') >= 0.75:
            return '我今年刚过22'

        return self.tuning(text_)

    def tuning(self, text_):
        '''图灵机器人'''
        # postdata['results'][0]['values']['text'] = text_
        postdata["perception"]["inputText"]["text"] = text_
        res = requests.post('http://openapi.tuling123.com/openapi/api/v2', json=postdata).text
        json_res = json.loads(res)
        turing_information = json_res['results'][0]['values']['text']

        return turing_information


# baidu_ai.speech_synthesis("""十年生死两茫茫，不思量，自难忘。千里孤坟，无处话凄凉。纵使相逢应不识，尘满面，鬓如霜。
# 夜来幽梦忽还乡，小轩窗，正梳妆。相顾无言，惟有泪千行。料得年年肠断处，明月夜，短松冈。""")

# baidu_ai.speech_recognition()


# a = baidu_ai.tuning('我是你爸爸')
# print(a)


if __name__ == '__main__':
    def dialogue(text):
        baidu_ai = Baidu_AI()
        # 图灵
        retrbot = baidu_ai.natural_language(text)
        # 制作mp3
        makingmp3 = baidu_ai.speech_synthesis(retrbot)
        # mp3to 转为文字
        robot_text = baidu_ai.speech_recognition(makingmp3)
        print(robot_text)


    res = dialogue('天气')
