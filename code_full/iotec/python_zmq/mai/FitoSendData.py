#from picamera import PiCamera,Color
from time import sleep
import zmq
import sys
from random import random
import base64
import time,datetime
import json

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class FitoSendData:

 def sendData(self, id_device, id_planta, url_image0, url_image1, mydatavars, ip, numport, lat, lng):
  port = numport
  if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

  if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

  context = zmq.Context()
  print "Connecting to server..."
  print ip
  print port
  socket = context.socket(zmq.REQ)
  socket.connect ("tcp://"+ ip + ":%s" % port)

  # toma lateral - 0

  image=open(url_image0,"rb")
  image_read=image.read()
  print("enviando imagen lat.jpg")
  pack = (image_read)

  socket.send(image_read)
  message_url0=socket.recv()
  print message_url0
  
  # toma lateral - 1

  image=open(url_image1,"rb")
  image_read=image.read()
  print("enviando imagen 1 .jpg")
  pack = (image_read)
    #for dato in pack:
  socket.send(image_read)
  message_url1=socket.recv()
  print message_url1
  


  today = '%s' % datetime.datetime.now()
  print today

  data_vars = Object()       

  data_vars.code_device = id_device
  data_vars.id_planta = id_planta
    
  data_vars.fecha = today
  data_vars.urlImageLat = message_url0
  data_vars.urlImageSup = message_url1
  
  data_vars.values = Object() 
  data_vars.values.ph = mydatavars.ph
  data_vars.values.temp = mydatavars.temp
  data_vars.values.ce = mydatavars.ce
  data_vars.values.o2 = mydatavars.o2
  data_vars.values.co2 = mydatavars.co2

  data_vars.values.LAT = lat
  data_vars.values.LONG = lng



  vars = data_vars.toJSON()
  print vars

  socket.send(vars)
  message=socket.recv()
  print message

  socket.close()

  return message
