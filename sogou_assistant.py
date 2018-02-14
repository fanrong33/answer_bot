# encoding: utf-8
# 由 Brain 实时获取搜狗API接口并入数据库

import requests
import json
import base64
import urllib.parse
from pymongo import MongoClient


def fetch_answer(key):
    """
    调用搜狗搜索答题助手API
    key: xigua 百万英雄
    """
    headers = {'Accept': '*/*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'Referer': 'https://assistant.sogoucdn.com/v5/cheat-sheet?channel=cddh&icon=http%3A%2F%2Fapp.sastatic.sogoucdn.com%2Fdati%2Fcd.png&name=%E5%86%B2%E9%A1%B6%E5%A4%A7%E4%BC%9A&appName=%E5%86%B2%E9%A1%B6%E5%A4%A7%E4%BC%9A',
               'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 Sogousearch/Ios/5.9.8',
               'Cookie': 'APP-SGS-ID=3wlRoSTVeiXNGlDZThdC6PkupfFPZKCF'}
    params = {
        'key': key,
        'wdcallback': 'jQuery20009925516224466264_1518438995829'
    }
    response = requests.get(url='https://wdpush.sogoucdn.com/api/anspush', headers=headers, params=params)
    print(response.status_code)
    content = response.text

    # 截取 json 字符串区间
    json_str = content[content.find('(')+1: len(content)-1]

    # js: o.result=JSON.parse(decodeURIComponent(escape(window.atob(o.result)))
    data = json.loads(json_str)

    decode = base64.b64decode(data['result'])
    decode = decode.decode('utf-8')

    result   = json.loads(urllib.parse.unquote(decode))
    question = json.loads(result[1])
    

    # 存储到数据库中
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.test

    data = {
        'cd_id'       : question['cd_id'],
        'channel'     : question['channel'],
        'title'       : question['title'],
        'answers'     : question['answers'],
        'choices'     : question['choices'],
        # 'has_answer'  : 1 if question['hasAnswer']==True else 0,
        'recommend'   : question['recommend'],
        'result'      : question['result'],
        'search_infos': question['search_infos'],
        'timestamp'   : int(time.time())
    }

    where = {'cd_id': question['cd_id']}
    if db.questions.find_one(where) == None:
        db.questions.save(data)



if __name__ == '__main__':
    import time
    
    # 每隔100毫秒获取一次最新的答案提示（使用4G网络）
    while True:
        fetch_answer('xigua')
        time.sleep(0.1)


