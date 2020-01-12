import paho.mqtt.client as mqtt
import sys
import time


class MqttClient:
    """
    MqttClient is a class which can be used to test MQTT quickly
    """
        
    def __init__(self,host,port=1883):
        self.__host = host
        self.__port = port
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connnect
        self.__client.on_message = self.__on_message
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_subscribe = self.__on_subscribe   
        self.__client.on_publish = self.__on_publish
        self.__bPublishCompleted = False

    def __on_connnect(self,client, userdata, flags, rc):    
        print("")
        print("Connected, result:%d" % rc)
        
    def __on_message(self,client, userdata, msg):
        print("")
        print("Message:")
        print("  Topic:" + msg.topic)
        print("Payload:" + str(msg.payload))
        
    def __on_disconnect(self,client, userdata, rc):
        print("")
        print("Disconnected:")
        
    def __on_subscribe(self,client, userdata, mid, granted_qos, properties):
        pass
        
    def __on_publish(self,client, userdata, mid):
        print("")
        print("Published:")            
        self.__bPublishCompleted = True
    
    def subscribeAndWaitMsg(self,topic,timeout=60,qos=2):
        """
        subscribe a topic, and wait for a timeout,if message of topic received, show it
        """        
        self.__client.connect(self.__host, self.__port, 5)
        
        tmBgn=time.time()
        bMsgSubscribed=False
        
        while time.time()-tmBgn < timeout:        
            if self.__client.is_connected():
                if not bMsgSubscribed:                    
                    print("subscribe %s" % topic)
                    self.__client.subscribe(topic,qos)
                    self.__client.loop()                    
                    bMsgSubscribed = True                

            self.__client.loop()
           
        print("")     
        print("Work completed!")
        self.__client.disconnect()
    
    def publishMsg(self,topic,payload,timeout=10):
        """
        Publish a message with topic and payload, then quit.
        """
        self.__client.connect(self.__host, self.__port, 5)
        bMsgPublished=False
        tmBgn=time.time()
        while time.time()-tmBgn < timeout and not self.__bPublishCompleted:
            if self.__client.is_connected():
                if not bMsgPublished:
                    print("publish topic %s, payload:%s"%(topic,payload))
                    self.__client.publish(topic,payload)
                    bMsgPublished = True            
            self.__client.loop()
            
        if self.__bPublishCompleted:
            print("Message had been Published")
        else:
            print("Failed")
            
        self.__client.disconnect()        

if __name__ == "__main__":
    
    if len(sys.argv) >= 4:
        if sys.argv[1] == '-s':
            client = MqttClient("192.168.0.10")
            client.subscribeAndWaitMsg(sys.argv[2],int(sys.argv[3]))
                
        elif sys.argv[1] == '-p':
            client = MqttClient("192.168.0.10")
            client.publishMsg(sys.argv[2],sys.argv[3])
    else:
        print("""
        Usage:    mqttclient -s topic timeout
                  mqttclient -p topic payload
        """)
