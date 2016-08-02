import json
import uuid
import base64
from urllib.request import Request, urlopen, HTTPError, URLError

mac_address=uuid.UUID(int=uuid.getnode()).hex[-12:]
url = "http://vop.baidu.com/server_api"
access_token = "24.2de162e4a21f37d66dc8276ed4d21eb0.2592000.1472696088.282335-8449392"
with open("wave.wav", 'rb') as f:
    spee = f.read()
    base64_wave = base64.b64encode(spee).decode("utf-8")
length = len(spee)

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
json_length = len(json_data)

header = {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-length': json_length,
}

req = Request(url, data=json_data, headers=header)
try:
    res = urlopen(url=req)
    print(res.read().decode())
except URLError or HTTPError as err:
    print(err)

