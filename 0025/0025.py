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
apikey = "TQGa9ibae2GoWHHQEU2WvoAN"     # 百度语音应用的API KEY
secretkey = "d58cf41ac479d2ed6d6afcf309170d16"      # 百度语音应用的 SECRET KEY
u1 = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&"


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


def get_access_token():
    u2 = u1 + "client_id=" + apikey + "&client_secret=" + secretkey + "&"
    try:
        di = eval(urlopen(u2).read())
        return di['access_token']
    except URLError or HTTPError as err0:
        print(err0)


def speech_text(wav, access_token="24.20b7b145256cbc85e011bc04cdbd4f90.2592000.1473914363.282335-8449392"):
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
    handle_text(speech_text("wave.wav", get_access_token()))