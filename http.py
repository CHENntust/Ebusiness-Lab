# -*- coding: utf-8 -*-
class Http():
    http_options = None
    resource_info = None
    callbacks=None
    def __init__(self):
        print("new http protocal")
    def read_resource(self,resfile):
        global resource_info, http_options
        with open(resfile, 'r') as f:
            data = f.read()
            resource_info = json.loads(data)
            http_options = {
                'host' : str(resource_info['host'][0]),
                'port' : int(resource_info['port']),
                'headers' : {
                    "Content-type": "application/json",
                    "Requesterid": str(resource_info['requesterid']),
                    "Access-Token": str(resource_info['accesstoken'])
                },
                'client_id' : str(resource_info['clientId']),
                'verify' : False
            }
        f.close()
        print("HOST : " + str(http_options['host']))
        print("PORT : " + str(http_options['port']))
        print("REQUESTER_ID : " + http_options['headers']['Requesterid'] + " ACCESS_TOKEN : " + http_options['headers']['Access-Token']) 
        print("finish setup")
        return http_options


    def publish_by_id(self,resource_id, value):
        """
        publish message to QIoT Suite Lite application by resource id.
        :param resource_id : input resource id
        :param value : input message will publish
        """
        resources = resource_info['resources']
        for res in resources:
            if (resource_id == str(res["resourceid"])) :
                #try:
                if 1 == 1:
                    url = 'http://' + http_options['host']+':'+str(http_options['port'])+'/resources/'+str(res["topic"])
                    print(url)
                    r = requests.post(url, headers=http_options['headers'], verify=False, data=json.dumps({'value': value}))
                    print("NOW TOPIC_NAME :" + str(res["topic"]) + " MESSAGE : " + str(value))
                #except:
                    #print('error')
                break
            elif res==resources[-1]:
                print("can't find the id " + resource_id + " in resourceinfo file")

    def publish_by_topic(self,topic, value):
        """
        publish message to QIoT Suite Lite application by resource topic.
        :param resource_id : input resource topic
        :param value : input message will publish
        """
        try:
            url = 'http://' + http_options['host']+':'+str(http_options['port'])+'/resources/'+str(topic)
            r = requests.post(url, headers=http_options['headers'], verify=False, data=json.dumps({'value': value}))
            print("NOW TOPIC_NAME :" + str(topic) + " MESSAGE : " + str(value))
        except:
            print('error')

    def subscribe_by_id(self,resource_id):
        """
        subscribe resource message by resource id
        :param resource_id : input resource id
        """
        resources = resource_info['resources']
        for res in resources:
            if (resource_id == str(res["resourceid"])) :
                try:
                    url = 'http://' + http_options['host']+':'+str(http_options['port'])+'/resources/'+str(res["topic"])
                    res = requests.get(url, headers=http_options['headers'], verify=False)
                    if(res.text!=None or res.text!="Not found"):
                        data={
                            'message': res.text,
                            'id':resource_id
                        }
                        self.trigger("message",data);
                    
                except:
                    print("subscribe_by_id error=")
                break
            elif res==resources[-1]:
                print("can't find the id " + resource_id + " in resourceinfo file")

    def get_topic_by_id(self, resource_id):
        resources = resource_info['resources']
        for res in resources:
            if (resource_id == str(res["resourceid"])):
                return str(res["topic"])
            elif res==resources[-1]:
                print("can't find the id " + resource_id + " in resourceinfo file")

    def on(self, event_name, callback):
        if self.callbacks is None:
            self.callbacks = {}

        if event_name not in self.callbacks:
            self.callbacks[event_name] = [callback]
        else:
            self.callbacks[event_name].append(callback)
    
    def trigger(self, event_name,data):
        if self.callbacks is not None and event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(self,data)
                
def connection(type):
    client = None
    if type == protocol.MQTT:
        from lib import mqtt_connect
        client = mqtt_connect.Mqtt()
    elif type == protocol.HTTP:
        #from lib import http_connect
        client = Http()
    elif type == protocol.HTTPS:
        from lib import https_connect
        client = https_connect.Https()
    elif type == protocol.COAP:
        from lib import coap_connect
        client = coap_connect.Coap()
    return client

class protocol:
    MQTT = "MQTT"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    COAP = "COAP"
    def __init__(self):
        print('define protocol')
    
import os
import random
import time
import json
import requests
print(requests.get('https://www.kite.com/python/answers/how-to-print-all-the-attributes-of-an-object-in-python'))
connection = connection(protocol.HTTP)
connection_options = connection.read_resource('./res/resourceinfo.json')
while 1:
    connection.publish_by_id("t", str(random.randint(0, 41)))
    time.sleep(1)
