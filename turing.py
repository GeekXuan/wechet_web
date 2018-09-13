import requests

KEY = '787904f3710043d8a17b207076953f14'


def get_response(msg):
    apiurl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(apiurl, data=data).json()
        if msg == r.get('text'):
            return '啊哦，snoopy不想理你并且去看动画片了...'
        else:
            return r.get('text')
    except:
        return "啊哦，snoopy可能睡着了..."
