# -*- coding: utf-8 -*-
import os
import web
import time
import datetime
import hashlib
from lxml import etree
import logging
import urllib2
import json
from urllib2 import HTTPError, URLError
API_YEELINK = '74c4601f0870e71ed6db8ec6f4741b33'
URL_RPI_SERSOR = 'http://api.yeelink.net/v1.0/device/350381/sensor/393171/datapoints'
URL_WEATHER_SENSOR = 'http://api.yeelink.net/v1.0/device/357151/sensor/405136/datapoints'
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

def get_sensor_data_acc(year,month,day,hour,minute,sec,url): #获取普通数值型传感器历史数据
    time_stamp = datetime.datetime(year,month,day,hour,minute,sec).isoformat()
    post_head = {"U-ApiKey": API_YEELINK}
    req = urllib2.Request(str(url+time_stamp+"/"),headers =post_head)
    try : response = urllib2.urlopen(req)
    except HTTPError as e:
        print "HTTP 连接出错，检查请求内容"
        print e.reason
        print e.code
    except URLError as e:
        print "报错内容:",
        print e.reason
        print "请求的网页错误，请检查网络连接"
        return 1
    except e:
        print "存在异常，函数退出"
        return 1
    js = json.loads(response.read())
    logging.warning(js)
    return str(js['value'])

def get_sensor_data(url): #获取普通数值型传感器历史数据
    post_head = {"U-ApiKey": API_YEELINK}
    req = urllib2.Request(str(url+"/"),headers =post_head)
    try : response = urllib2.urlopen(req)
    except HTTPError as e:
        print "HTTP 连接出错，检查请求内容"
        print e.reason
        print e.code
    except URLError as e:
        print "报错内容:",
        print e.reason
        print "请求的网页错误，请检查网络连接"
        return 1
    except e:
        print "存在异常，函数退出"
        return 1
    js = json.loads(response.read())
    logging.warning(js)
    str = js['value'] + u"   (数据更新时间)" + js['timestamp']
    #return str(js['value'])
    return str

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
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        logging.warning(msgType)  
        if(msgType=='voice'):
            MediaID=xml.find("MediaId").text
            logging.warning(u"媒体ID"+MediaID)
            return self.render.reply_text(fromUser,toUser,int(time.time()),u"返回媒体ID:"+MediaID) 
        elif(msgType=='text'):
            content=xml.find("Content").text   #判断为文字才做文字处理
            if u'树莓派温度' in content:
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"当前树莓派的温度是:"+get_sensor_data(URL_RPI_SERSOR)) 
            if u'温度' in content:
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"当前 平台 气象站 的温度是:"+get_sensor_data(URL_WEATHER_SENSOR)) 
            elif u'气压' in content:
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"t当前 平台 NULL 的气压是:"+"103k pa") 
            elif u'平台' in content:
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"当前 选中的平台是 NULL") 
            elif u'green' in content:
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"当然是选择原谅她啦！") 
            return self.render.reply_text(fromUser,toUser,int(time.time()),u"你刚才发送到公众号的信息是:"+content) 
        

app = web.application(urls, globals())
application = app.wsgifunc()
if __name__ == "__main__":
    application.run()