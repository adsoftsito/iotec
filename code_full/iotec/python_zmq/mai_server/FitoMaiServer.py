import signal
import zmq
import six
import base64
import requests
import json
from time import sleep
from google.cloud import storage
from google.cloud import datastore
import datetime

if __name__ == '__main__':

 ctx = zmq.Context()
 socket = ctx.socket(zmq.REP)
 socket.bind("tcp://*:3000")
 print(" ")
 print("--------------Fitotron SERVER READY -------------") 

while True:

    message = socket.recv()
    if message.startswith('{'):
     # It's a string !!
     myparams = json.loads(message)

     pars = {
      "code_device": myparams['code_device'],
      "id_planta": myparams['id_planta'],
      "fecha": myparams['fecha'],
      "values": json.dumps(myparams['values']),  # users=[{"email_hash": "fh7834uifre8houi3f"}, ... ]
      "urlImageLat": myparams['urlImageLat'],
      "urlImageSup": myparams['urlImageSup']
     }
     r = requests.get("http://fitotron-api.appspot.com/sendSensado", params= pars)
     data = r.text
     re = "inserted ok"
 
     socket.send(re)

    else:
     img_recv = (message)
     img_result = open('imagen.jpg', 'w')
     img_result.write(img_recv)
     print("Image  recived")


     client = storage.Client()
     bucket = client.get_bucket('fitotron-api.appspot.com')
     #print  "--- bucket name ---"
     #print bucket

     today = '%s' % datetime.datetime.now()
     today = today.replace(' ', '_')
     today = today.replace(':', '_')
     today = today.replace('.', '_')
     print today

     blob = bucket.get_blob('imagen.jpg')
     urlblob = "mr3_%s.jpg" % today
     blob = bucket.blob(urlblob)
     print blob
     blob.upload_from_filename('./imagen.jpg')
     url = blob.public_url
     print('Blob '+ url)

     # Get the feed



     re = url
     socket.send(re)
