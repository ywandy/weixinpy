# coding=UTF-8
import os
import web              #web.py
import time
import datetime
import hashlib          #hash�����㷨
from lxml import etree  #xml����
import requests         #http����
import json
import codecs           

#===================΢�Ź����˺���Ϣ================================
#��΢�ſ���ҳ���е������Ϣ��������ַ�����ʽ
my_appid = 'wx3ff393e05c40ba87'
my_secret = '099eb97db9420ea2b492e15d2e7272de'
#========ƥ��URL��������ʽ,url/����WeixinInterface�ദ��===========
urls = ( '/','WeixinInterface' )

#===================΢��Ȩ�޽���====================================
def _check_hash(data):
    '''
    ��Ӧ΢�ŷ��͵�GET����(HashУ��)
    :param data: ���յ�������
    :return: True or False���Ƿ�ͨ����֤
    '''
    signature=data.signature  #����ǩ��
    timestamp=data.timestamp  #ʱ���
    nonce=data.nonce          #�����
    #�Լ���token
    token="123456"   #�����д����΢�Ź���ƽ̨�������token
    #�ֵ�������
    list=[token,timestamp,nonce]
    list.sort()   #ƴ�ӳ�һ���ַ�������sha1����,���ܺ���signature���жԱ�
    sha1=hashlib.sha1()
    map(sha1.update,list)
    hashcode=sha1.hexdigest() #sha1�����㷨
    #���������΢�ŵ�������ظ�echostr
    if hashcode == signature:
        return True
    return False

#=====================΢��+HTTP server===============================
class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def _reply_text(self, toUser, fromUser, msg):
        '''
        �ظ��ı���Ϣ
        :param fromUser:
        :param toUser:
        :param msg:what you sent
        :return:
        '''
        return self.render.reply_text(toUser, fromUser, int(time.time()),msg + '\n\ntime: ' + now_time)#����ʱ���

    def _recv_text(self, fromUser, toUser, xml):
        '''
       auto reply
        :param fromUser:
        :param toUser:
        :param xml:rec xml
        :return:
        '''
        #��ȡxml��Content�ı���Ϣ
        content = xml.find('Content').text
        reply_msg = content
        return self._reply_text(fromUser, toUser, u'you said��' + reply_msg )

    def GET(self): #get,��ָ������Դ��������
        #��ȡ�������
        data = web.input()
        if _check_hash(data):
            return data.echostr #΢�ŷ���������ַ���,����֤ͨ��,�򷵻�echostr

    def POST(self): #post,��ָ������Դ�ύ����
        str_xml = web.data() #���post��������
        xml = etree.fromstring(str_xml)#����XML����
        msgType=xml.find("MsgType").text #��Ϣ����,����text/event/image/voice/location/link��
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        #�Բ�ͬ���͵���Ϣ�ֱ���:
        if msgType == 'text':
            return self._recv_text(fromUser, toUser, xml)

#=====================����app========================================

if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()