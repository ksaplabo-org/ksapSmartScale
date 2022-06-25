import paho.mqtt.client
import json
import ssl
import time

# Mqtt Define
AWSIoT_ENDPOINT = "alij9rhkrwgll-ats.iot.ap-northeast-1.amazonaws.com"
MQTT_PORT = 8883
MQTT_TOPIC_PUB = "topicSmartZaikoPub"
MQTT_TOPIC_SUB = "topicSmartZaikoSub"
MQTT_ROOTCA = "/home/pi/Downloads/AmazonRootCA1.pem"
MQTT_CERT = "/home/pi/Downloads/b560ab69ea7216d5610dc6bfcb124bbdfe5934e3a71b41dc018dbde431186011-certificate.pem.crt"
MQTT_PRIKEY = "/home/pi/Downloads/b560ab69ea7216d5610dc6bfcb124bbdfe5934e3a71b41dc018dbde431186011-private.pem.key"
MQTT_CONNECT_RETRY = 5

class AWSSender:

    def __init__(self):
        self.__client = paho.mqtt.client.Client()
        self.__client.on_connect = self.__mqtt_connect
        self.__client.on_message = self.__mqtt_message
        self.__client.tls_set(
                MQTT_ROOTCA, 
                certfile=MQTT_CERT, 
                keyfile=MQTT_PRIKEY, 
                cert_reqs=ssl.CERT_REQUIRED, 
                tls_version=ssl.PROTOCOL_TLSv1_2, 
                ciphers=None)
        self.__is_connected = False

    def __mqtt_connect(self, client, userdata, flags, respons_code):
        print('mqtt connected.') 
        client.subscribe(MQTT_TOPIC_SUB)
        self.__is_connected = True
        print('subscribe topic : ' + MQTT_TOPIC_SUB) 

    def __mqtt_message(self, client, userdata, msg):
        # Get Received Json Data 
        json_dict = json.loads(msg.payload)

    def putHarai(self ,haraiList):

        if haraiList.count == 0: return

        self.__client.connect(AWSIoT_ENDPOINT, port=MQTT_PORT, keepalive=60)
        time.sleep(1)

        for harai in haraiList:
            data = json.dumps({"datetime":harai['datetime'],
                                "id":harai['zaiko']['id'],
                                "haraisu":harai['haraisu'],
                                "zaikosu":harai['zaikosu'],
                                "scaleWeight":harai['scaleWeight'] 
                                })
            self.__client.publish(MQTT_TOPIC_PUB ,data)

        self.__client.disconnect()