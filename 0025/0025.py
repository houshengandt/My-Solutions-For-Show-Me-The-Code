import wave
import pyaudio
import json
import uuid
import base64
import webbrowser
from urllib.request import Request, urlopen, HTTPError, URLError


#网站列表
website  = {
    'www.baidu.com': 'ｂａｉｄｕ，baidu,百度,白度,白，度，b a i d u, ｂａｉｄｕ，',
    'www.weibo.com': "微博，微，博",
    'www.google.com': '谷歌，谷，歌，'
}

# 录音阶段常量
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "wave.wav"


# 识别阶段常量
mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
url = "http://vop.baidu.com/server_api"
access_token = "24.2de162e4a21f37d66dc8276ed4d21eb0.2592000.1472696088.282335-8449392"


def record_wave(p):
    # 参考 pyaudio 文档例子
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* 正在录音......")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* 录音完毕......")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def speech_text(wav):
    with open(wav, 'rb') as f:
        spee = f.read()
        base64_wave = base64.b64encode(spee).decode("utf-8")

    length = len(spee)    # 需要提供原始文件长度

    content = {
        "format": "wav",
        "rate": 8000,
        "channel": '1',
        "token": access_token,
        "cuid": mac_address,
        'lan': 'zh',
        "len": length,
        "speech": base64_wave,
    }

    json_data = json.dumps(content).encode('utf-8')
    json_length = len(json_data)    # 要写在header的Content-length里

    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-length': json_length,
    }

    req = Request(url, data=json_data, headers=header)
    try:
        print("* 正在上传录音......")
        res = urlopen(url=req)
        resp = res.read().decode()
        return resp
    except URLError or HTTPError as err:
        print("* 录音上传失败......")
        print(err)


def handle_text(tex):
    tex1 = tex.replace('[', '')
    tex2 = tex1.replace(']', '')
    dic = eval(tex2)
    result = dic['result']
    print("* 识别结果：" + result)
    for key, value in website.items():
        if result in value:
            webbrowser.open(key)
            print("* 正在打开:" + key)
            break
    else:
        print("* 失败......")


if __name__ == "__main__":
    record_wave(pyaudio.PyAudio())
    handle_text(speech_text("wave.wav"))