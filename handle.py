# -*- coding: utf-8 -*-
# filename: handle.py

import web
import logging
from wechatpy import parse_message
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TextReply, ImageReply
from wechatpy.client import WeChatClient

import pics
from ash_spider_db import search
from turing import get_response
from xlzx import get_link

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/root/projects/wechat_web/log/debug.log', mode='a')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s -- %(levelname)s -- %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                logger.info(web.url() + ' access without data')
                return "wrong access"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = 'snoopytx20180412'
            try:
                check_signature(token, signature, timestamp, nonce)
                # print(web.url() + 'data: ' + str(data) + ' get: ' + nonce + ' return: ' + echostr)
                logger.info(web.url() + 'data: ' + str(data) + ' get: ' + nonce + ' return: ' + echostr)
                return echostr
            except InvalidSignatureException as e:
                logger.warning(web.url() + ' ' + e + ' wrong signature')
                # print('wrong signature')
        except Exception as Argument:
            # print(web.url() + ' data: ' + str(data) + ' get: ' + nonce + ' return: ' + Argument)
            logger.warning(web.url() + ' wrong: ' + str(Argument))
            return False

    def POST(self):
        try:
            xml = web.data()
            msg = parse_message(xml)
            if msg.type == 'text':
                content = msg.content
                if content.startswith(('表情包:', '表情包：')):
                    words = ''.join(content.replace('：', ':').split(':')[1:])
                    wechat_client = WeChatClient(
                        appid='wx19a2591b2a719add',
                        secret='c46fa65dbc2803b90431fbf9c803cbd4',
                    )
                    access_token = wechat_client.access_token
                    json_data = pics.upload_pic(pics.get_random_pic(words), access_token)
                    # print(json_data)
                    if 'errcode' not in json_data:
                        media_id = json_data['media_id']
                        reply = ImageReply(message=msg)
                        reply.media_id = media_id
                        # print(web.url() + ' get_pic. words: ' + words + ' return: ' + str(json_data))
                        logger.info(web.url() + ' get_pic. words: ' + words + ' return: ' + str(json_data))
                    else:
                        reply = TextReply(message=msg)
                        reply.content = json_data['link']
                        logger.warning(web.url() + ' get_pic faild,return link.  words:' + words + ' return: ' + json_data['link'])
                elif content.startswith(('影视:', '影视：')):
                    words = ''.join(content.replace('：', ':').split(':')[1:])
                    if words == '':
                        string = '没有输入要搜索的名字！'
                        logger.info(web.url() + ' get_movie without words')
                    else:
                        data = search(words)
                        data1 = data[0]
                        data2 = data[1]
                        if len(data1) != 0:
                            string = ''
                            if len(data1) <= 12:
                                for each in data1:
                                    string += '%s %s %s %s\n' % (each[0], each[1], each[3], each[4])
                            else:
                                for each in data1[:12]:
                                    string += '%s %s %s %s\n' % (each[0], each[1], each[3], each[4])
                        elif len(data2) != 0:
                            string = ''
                            if len(data2) <= 12:
                                for each in data2:
                                    string += '%s %s %s %s\n' % (each[0], each[1], each[3], each[4])
                            else:
                                for each in data2[:12]:
                                    string += '%s %s %s %s\n' % (each[0], each[1], each[3], each[4])
                        else:
                            string = '竟然没有搜索到！！！\n请检查名称输入的是否正确，请尽量使用中文哦'
                        # print(web.url() + ' get_pic. words: ' + words + ' data: ' + str(data) + ' return: ' + string)
                        logger.info(web.url() + ' get_movie. words: ' + words + ' data: ' + str(data) + ' return: ' + string)
                    reply = TextReply(message=msg)
                    reply.content = string
                elif content.startswith(('在线:', '在线：')):
                    words = ''.join(content.replace('：', ':').split(':')[1:])
                    if words == '':
                        string = '没有输入要搜索的名字！'
                        logger.info(web.url() + ' see_movie without words')
                    else:
                        data = get_link(words)
                        if data:
                            string = data
                        else:
                            string = '竟然没有搜索到！！！\n请检查名称输入的是否正确，请试试英文名哦'
                        # print(web.url() + ' see_pic. words: ' + words + ' data: ' + str(data) + ' return: ' + string)
                        logger.info(web.url() + ' see_movie. words: ' + words + ' data: ' + str(data) + ' return: ' + string)
                    reply = TextReply(message=msg)
                    reply.content = string
                else:
                    reply = TextReply(message=msg)
                    response = get_response(content)
                    logger.info(web.url() + ' turing. words: ' + content + ' response: ' + response)
                    reply.content = response
            elif msg.type == 'event' and msg.event:
                mscontent = msg.event
                if mscontent == "subscribe":
                    string = '终于等到你！欢迎关注Snoopy同学~\n' \
                             '输入"表情包：xxx"获取自定义文字的表情\n' \
                             '输入"影视：xxx"获取电影的网盘链接\n' \
                             '输入"在线：xxx"获取在线观看视频的链接，需要复制到浏览器使用哦~'
                    reply = TextReply(message=msg)
                    reply.content = string
                elif mscontent == "unsubscribe":
                    string = '有什么不足之处还请谅解，我会慢慢改进，欢迎您以后再来'
                    reply = TextReply(message=msg)
                    reply.content = string
            # 转换成 XML
            reply_xml = reply.render()
            return reply_xml
        except Exception as e:
            logger.error(e)
            # print(e)
            return "success"



