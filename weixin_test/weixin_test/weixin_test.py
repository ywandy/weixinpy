# coding=UTF-8
import os
import web              #web.py
import time
import datetime
import hashlib          #hash加密算法
from lxml import etree  #xml解析
import requests         #http请求
import json
import codecs           

#===================微信公众账号信息================================
#把微信开发页面中的相关信息填进来，字符串格式
my_appid = 'wx3ff393e05c40ba87'
my_secret = '099eb97db9420ea2b492e15d2e7272de'
#========匹配URL的正则表达式,url/将被WeixinInterface类处理===========
urls = ( '/','WeixinInterface' )

#===================微信权限交互====================================
def _check_hash(data):
    '''
    响应微信发送的GET请求(Hash校验)
    :param data: 接收到的数据
    :return: True or False，是否通过验证
    '''
    signature=data.signature  #加密签名
    timestamp=data.timestamp  #时间戳
    nonce=data.nonce          #随机数
    #自己的token
    token="123456"   #这里改写你在微信公众平台里输入的token
    #字典序排序
    list=[token,timestamp,nonce]
    list.sort()   #拼接成一个字符串进行sha1加密,加密后与signature进行对比
    sha1=hashlib.sha1()
    map(sha1.update,list)
    hashcode=sha1.hexdigest() #sha1加密算法
    #如果是来自微信的请求，则回复echostr
    if hashcode == signature:
        return True
    return False

#=====================微信+HTTP server===============================
class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def _reply_text(self, toUser, fromUser, msg):
        '''
        回复文本消息
        :param fromUser:
        :param toUser:
        :param msg:what you sent
        :return:
        '''
        return self.render.reply_text(toUser, fromUser, int(time.time()),msg + '\n\ntime: ' + now_time)#加入时间戳

    def _recv_text(self, fromUser, toUser, xml):
        '''
       auto reply
        :param fromUser:
        :param toUser:
        :param xml:rec xml
        :return:
        '''
        #提取xml中Content文本信息
        content = xml.find('Content').text
        reply_msg = content
        return self._reply_text(fromUser, toUser, u'you said：' + reply_msg )

    def GET(self): #get,从指定的资源请求数据
        #获取输入参数
        data = web.input()
        if _check_hash(data):
            return data.echostr #微信发来的随机字符串,若验证通过,则返回echostr

    def POST(self): #post,向指定的资源提交数据
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        msgType=xml.find("MsgType").text #消息类型,包括text/event/image/voice/location/link等
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        #对不同类型的消息分别处理:
        if msgType == 'text':
            return self._recv_text(fromUser, toUser, xml)

#=====================启动app========================================

if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()