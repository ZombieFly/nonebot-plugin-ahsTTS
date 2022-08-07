from pydub import AudioSegment

import requests
import re
import os


class ahs_audio_down:

    def __init__(self, intxt) -> None:
        #
        #   输入待合成文本，输出音频id
        #
        url = 'https://cloud.ai-j.jp/demo/aitalk2webapi_nop.php'
        d = {'speaker_id': '553', 'text': intxt}
        audio_url = requests.post(url, data=d).text

        print(audio_url)
        pattern = re.compile(r'tmp\\/'+'(.*?)'+".mp3")
        data = pattern.findall(audio_url)
        self.id = data[0]
        return

    def get_audio(self) -> str:
        #
        #   输入音频id，下载源音频文件，返回文件名
        #
        res = requests.get(f'https://cloud.ai-j.jp/demo/tmp/{self.id}.mp3')
        with open(f'./record/{self.id}.mp3', 'wb') as code:
            code.write(res.content)
            code.flush()

        self.path = os.path.abspath(f'./record/{self.id}.mp3')
        return self.path

    def cut(self) -> str:
        #
        #   输入源文件，剪切掉前3.3s
        #
        sound = AudioSegment.from_mp3(self.path)

        sound = sound[3300:]
        outfile = './record/outfile.mp3'

        # 扩大音量
        sound = sound.apply_gain(+20)

        sound.export(outfile, format="mp3")
        self.path = os.path.abspath(outfile)
        return self.path
