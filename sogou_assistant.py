# encoding: utf-8
# 由 Brain 实时获取搜狗API接口并入数据库

import requests
import json
import base64
import urllib.parse

def fetch_answer(key):
    headers = {'Accept': '*/*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'Host':'zhannei.baidu.com',
               'Referer': 'https://assistant.sogoucdn.com/v5/cheat-sheet?channel=cddh&icon=http%3A%2F%2Fapp.sastatic.sogoucdn.com%2Fdati%2Fcd.png&name=%E5%86%B2%E9%A1%B6%E5%A4%A7%E4%BC%9A&appName=%E5%86%B2%E9%A1%B6%E5%A4%A7%E4%BC%9A',
               'Cookie': 'APP-SGS-ID=3wlRoSTVeiXNGlDZThdC6PkupfFPZKCF',
               'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 Sogousearch/Ios/5.9.8'}
    # response = requests.get(url='https://wdpush.sogoucdn.com/api/anspush?key=xigua&wdcallback=jQuery20009925516224466264_1518438995829&_=1518438995830', headers=headers) # params={'wd': question + choices[i]}
    print(response.status_code)
    content = response.text
    content = 'jQuery20009925516224466264_1518438995829({"code": 0, "allow": true, "result": "WyJ7XCJhbnN3ZXJzXCI6W1wi56eB5oiRXCIsXCLotoXmiJFcIixcIuWkp+aIkVwiXSxcImNkX2lkXCI6XCJhbmRyb2lkX2J3eXhfMTUxODQ0ODg3NjUwMlwiLFwiY2hhbm5lbFwiOlwiYnd5eFwiLFwiY2hvaWNlc1wiOlwi56eB5oiROi0xfOi2heaIkTotMXzlpKfmiJE6LTFcIixcImRlYnVnXCI6XCJvZmZcIixcImhhc0Fuc3dlclwiOnRydWUsXCJyZWNvbW1lbmRcIjpcIui2heaIkVwiLFwicmVzdWx0XCI6XCLotoXmiJFcIixcInNlYXJjaF9pbmZvc1wiOlt7XCJzdW1tYXJ5XCI6XCLlvJfmtJvkvIrlvrforqTkuLrlrozmlbTnmoTkurrmoLznu5PmnoTnlLHkuInlpKfpg6jliIbnu4TmiJAs5Y2z5pys5oiR44CB6Ieq5oiR5ZKM6LaF5oiR44CCIOaJgOiwk+acrOaIkSzlsLHmmK/mnKwuLi4g5LuW6K+0OuKAnOeyvuelnuWIhuaekOeahOesrOS4gOS4quS7pOS6uuS4jeW/q+eahOWRvemimOaYrzrlv4PnkIbov4fnqIvkuLvopoHmmK/ml6DmhI/or4bnmoQs6Iez5LqO5oSP6K+G55qE6L+HLi4uXCIsXCJ0aXRsZVwiOlwi5byX5rSb5LyK5b6355qE5Lq65qC857uT5p6E55CG6K66IC0g5pCc54uX55m+56eRXCIsXCJ1cmxcIjpcImh0dHA6Ly9iYWlrZS5zb2dvdS5jb20vdjc2MjYzMDg4Lmh0bT9mcm9tVGl0bGU9JUU1JUJDJTk3JUU2JUI0JTlCJUU0JUJDJThBJUU1JUJFJUI3JUU3JTlBJTg0JUU0JUJBJUJBJUU2JUEwJUJDJUU3JUJCJTkzJUU2JTlFJTg0JUU3JTkwJTg2JUU4JUFFJUJBXCJ9XSxcInRpdGxlXCI6XCIxMS4g5byX5rSb5LyK5b6357K+56We5YiG5p6Q55CG6K666K6k5Li65Lq65qC857uT5p6E55Sx5LiJ6YOo5YiG57uE5oiQ77yM5LiL5YiX5ZOq5Liq6YCJ6aG55bGe5LqO6L+Z5LiJ6YOo5YiG5LmL5Lit77yfXCIsXCJ1aWRcIjpcIm51bGxfdXVpZFwifSIsIntcImFuc3dlcnNcIjpbXCLmsLTmiYsxMOWPt1wiLFwi5YWI6amx6ICFMTDlj7dcIixcIuacuumBh+WPt1wiXSxcImNkX2lkXCI6XCJhbmRyb2lkX2J3eXhfMTUxODQ0OTAxOTIyN1wiLFwiY2hhbm5lbFwiOlwiYnd5eFwiLFwiY2hvaWNlc1wiOlwi5rC05omLMTDlj7c6LTF85YWI6amx6ICFMTDlj7c6LTF85py66YGH5Y+3Oi0xXCIsXCJkZWJ1Z1wiOlwib2ZmXCIsXCJoYXNBbnN3ZXJcIjp0cnVlLFwicmVjb21tZW5kXCI6XCLmsLTmiYsxMOWPt1wiLFwicmVzdWx0XCI6XCLmsLTmiYsxMOWPt1wiLFwic2VhcmNoX2luZm9zXCI6W3tcInN1bW1hcnlcIjpcIuebruWJjeS6uuexu+WPkeWwhOeahOaOoua1i+WZqOW3sumjnuWHuuS6huWkqumYs+ezuyzlpoLmnpzmjqLmtYvlmajmiYDlj5flpJblipvlhajpg6jmtojlpLEs6YKj5LmI5o6i5rWL5Zmo5bCGKCApIEEu5rK/5Y6f6Lev5b6ERCDor5XpopjliIbmnpA654mb6aG/56ys5LiA5a6a5b6L5ZGK6K+J5oiR5LusOuS4gOWIh+eJqeS9k+WcqOS4jeWPl+WkluWKm+S9nOeUqOaXtizmgLvkv53mjIEuLi5cIixcInRpdGxlXCI6XCLnm67liY3kurrnsbvlj5HlsITnmoTmjqLmtYvlmajlt7Lpo57lh7rkuoblpKrpmLPns7ss5aaC5p6c5o6i5rWL5Zmo5omA5Y+X5aSW5Yqb5YWo6YOo5raILi4uXCIsXCJ1cmxcIjpcImh0dHBzOi8vemhpZGFvLmJhaWR1LmNvbS9xdWVzdGlvbi8yMTE3MDAxNjAzMzkwNzIxNzA3XCJ9XSxcInRpdGxlXCI6XCIxMi4g5Lq657G75Y+R5bCE55qE5ZOq5Liq5o6i5rWL5Zmo5bey57uP6aOe5Ye65LqG5aSq6Ziz57O777yfXCIsXCJ1aWRcIjpcIm51bGxfdXVpZFwifSJd"})'
    # 截取 json 字符串
    json_str= content[41:-1]
    # js: o.result=JSON.parse(decodeURIComponent(escape(window.atob(o.result)))
    data = json.loads(json_str)

    decode = base64.b64decode(data['result'])
    decode = decode.decode('utf-8')

    # encodeURIComponent
    result = json.loads(urllib.parse.unquote(decode))
    print(result[1])
    q = json.loads(result[1])
    print(q)
    print(q['answers'])
    print(q['search_infos'][0]['summary'])
    exit()


if __name__ == '__main__':
    fetch_answer('xigua')