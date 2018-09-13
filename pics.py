import requests
import random

PIC_IDS = [1, 10, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 3, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 4, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 55, 56, 57, 58, 6, 60, 62, 63, 65, 66, 67, 68, 69, 71, 73, 76, 77, 78, 81, 82, 83, 84, 85, 88, 89, 9, 90, 91, 92]


def get_pic(id_, text=''):
    url = 'https://www.52doutu.cn/api/?types=maker&id=%d&str1=%s' % \
          (id_, text)
    try:
        r = requests.get(url).content
        filename = 'temp/%d_%d.jpg' % (id_, random.randint(100000000, 1000000000))
        with open(filename, 'wb') as f:
            f.write(r)
        return filename
    except Exception as e:
        print(e)
        return url


def get_random_pic(text=''):
    num = random.sample(PIC_IDS, 1)[0]
    return get_pic(num, text)


def upload_pic(filename, access_token):
    if not filename.startswith('https://'):
        url = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image' % access_token
        files = {'media': open(filename, 'rb')}
        data = {'enctype': 'multipart/form-data', 'name': 'media', 'filename': filename}
        r = requests.post(url, data=data, files=files)
        return r.json()
    else:
        return {'errorcode': -1, 'link': '表情包无法在线生成，链接：' + filename}
        # return {'errorcode': -1, 'link': '表情包无法生成，请稍后再试'}


if __name__ == '__main__':
    get_random_pic(text='test')

