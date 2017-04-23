# -*- coding: utf-8 -*-
import os
import web
import time
import hashlib
from lxml import etree
 
 
urls = (
'/weixin','WeixinInterface'
)
 

def _check_hash(data):
    signature=data.signature
    timestamp=data.timestamp
    nonce=data.nonce
    token='1234567890'
    list=[token,timestamp,nonce]
    list.sort()
    sha1=hashlib.sha1()
    map(sha1.update,list)
    hashcode=sha1.hexdigest()

    if hashcode == signature:
        return True
    return False


class WeixinInterface:
 
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
 
    def GET(self):
        data = web.input()
        if _check_hash(data):
            return data.echostr

    def POST(self):        
        str_xml = web.data() 
        xml = etree.fromstring(str_xml)
        content=xml.find("Content").text
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if 'temp' in content:
             return self.render.reply_text(fromUser,toUser,int(time.time()),u"the tempture is:"+"99") 
        elif 'baro' in content:
             return self.render.reply_text(fromUser,toUser,int(time.time()),u"the baro is:"+"103k pa") 
         elif 'green' in content:
             return self.render.reply_text(fromUser,toUser,int(time.time()),u"当然是选择原谅她啦！") 
        return self.render.reply_text(fromUser,toUser,int(time.time()),u"what you sent:"+content) 
        

app = web.application(urls, globals())
application = app.wsgifunc()
if __name__ == "__main__":
    application.run()