import requests
import time
import hashlib
import uuid

youdao_url = 'https://openapi.youdao.com/api'


def translate(word):
    time_curtime = int(time.time())  # 秒级时间戳获取
    app_id = "646258019e11725a"  # 应用id
    uu_id = uuid.uuid4()  # 随机生成的uuid数，为了每次都生成一个不重复的数。
    app_key = "rGwfYBuyiJbdjZvmLUZfUPVUnV63pjoP"  # 应用密钥
    sign = hashlib.sha256(
        (app_id + word + str(uu_id) + str(time_curtime) + app_key).encode('utf-8')).hexdigest()
    data = {
        'q': word,  # 翻译文本
        'from': "auto",  # 源语言
        'to': "auto",  # 翻译语言
        'appKey': app_id,  # 应用id
        'salt': uu_id,  # 随机生产的uuid码
        'sign': sign,  # 签名
        'signType': "v3",  # 签名类型，固定值
        'curtime': time_curtime,  # 秒级时间戳
    }
    r = requests.get(youdao_url, params=data).json()  # 获取返回的json()内容

    if r['isWord']:
        print(r['basic']['explains'])
        return r['basic']['explains']
    else:
        print("None")
        return ' '
