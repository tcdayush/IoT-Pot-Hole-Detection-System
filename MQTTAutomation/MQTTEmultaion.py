#title           :thingsboardmqtt.py
#description     :Script to emulate the mqtt request and data transfer between sensor board and thingsboard
#author          :ayush mishra
#version         :1.4
#python_version  :3.7.0

import paho.mqtt.client as mqtt
import time,json,random

broker="http://localhost:8080"
port =8080

def on_log(client, userdata, level, buf):
   print(buf) 
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.loop_stop()  

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")

count=0
mqtt.Client.connected_flag=False
mqtt.Client.suppress_puback_flag=False
client = mqtt.Client("python1") 
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
username="Apx1r8fNNQbr9JILm3"
username="tuQaiUAtTxq3aUO2pw"
password=""
if username !="":
    client.username_pw_set(username, password)

client.connect(broker,port)
client.loop_start()
while not client.connected_flag:
   client.loop()
   print("In wait loop")
   time.sleep(1)
time.sleep(3)
print("publishing qos of 1")

class Sensor:
   def __init__(self, client, topic, qos, change, interval, direction,\
                start_value,min_value,max_value):
      self.client=client
      self.change_up=change
      self.change_down= -change
      self.change=change
      self.interval=interval
      self.temp=start_value
      self.max_value=max_value
      self.min_value=min_value
      self.direction=direction
      self.topic=topic
      self.qos=qos
      
   def random_change(self):
     a=random.randint(0,10)
     b=random.randint(0,25)
     print("direction =",self.direction)
     
     if b==6 and self.direction=="up": 
         self.direction="down"
     elif b==6 and self.direction=="down":
         self.direction="up"
       
     if self.direction=="up":
         self.change=self.change_up
     else:
         self.change=self.change_down    
     
     if a==5 and self.direction=="up":
          self.change=self.change_down
     elif a==5 and self.direction=="down":
         self.change=self.change_up
   
   def publish(self,data_out):
      print("data out=",data_out)
      self.client.publish(self.topic,data_out,self.qos)
      
   def update(self):
      self.random_change()
      self.temp=self.temp+self.change
   
   def start(self):
     while True:
         self.update()
         self.client.loop(0.01)
         
         if self.temp>=self.max_value:
             self.temp=self.max_value
         if self.temp<=self.min_value:
             self.temp=self.min_value

         if json_data_flag:
            data=dict()
            data["room-temp"]=self.temp
            data_out=json.dumps(data)
         else:
            data_out=self.temp
         
         self.publish(data_out)
         time.sleep(self.interval)

json_data_flag=True
topic="v1/devices/me/telemetry"
qos=0
change=0.5
interval=2
direction="up"
min_value=0
max_value=30
start_value=20
s=Sensor(client,topic,qos,change,interval,direction,start_value,min_value,max_value)
s.start()
     
client.disconnect()
