import zmq
import sys
import base64
import httplib, urllib
import json
import os

# server_api = "54.202.85.225"
server_api = "35.185.213.109";

# device = '590978bb812b610001f2344c';
device = '59ac7e37883f61000132ef87';

def obtenToken():
    params = urllib.urlencode({'name': 'adsoft', 'password': 'qubit'})
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(server_api, 8082)
    conn.request("POST", "/api/authenticate", params, headers)
    response = conn.getresponse()
    data = json.load(response)   
    return data['token']

def subeSensor(token, label, confidence):
    params = urllib.urlencode({'token': token, 'name': label, 'value':confidence})
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(server_api, 8082)
    conn.request("POST", "/api/device/" + device + "/sensor", params, headers)
    response = conn.getresponse()
    data = json.load(response)  
    if not data['success'] == True:
        print("Error subiendo " + label)

def subeImagen(token, label, id):
    params = urllib.urlencode({'token': token, 'label': label, 'ref':id})
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(server_api, 8082)
    conn.request("POST", "/api/device/" + device + "/sensor/img", params, headers)
    response = conn.getresponse()
    data = json.load(response)  
    if not data['success'] == True:
        print("Error subiendo " + label)

port = "3000"
server = server_api #"127.0.0.1"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    server =  sys.argv[2]



context = zmq.Context()
print "Connecting to server %s:%s" % (server, port)
path =  (os.path.dirname(os.path.realpath(__file__)))
socket = context.socket(zmq.REQ)
socket.connect ("tcp://%s:%s" % (server, port))

f = open( path + "/test1.jpg",'rb')
bytes = bytearray(f.read())
strng = base64.b64encode(bytes)
socket.send(strng)
message = socket.recv()

labels = message[0:message.find("(") - 1].split(',')
confidence = message[message.find("(")+1:message.find(")")].split(" ")[2]
img_id = message[message.find("[")+1:message.find("]")]

print labels
print confidence

token = obtenToken()
for label in labels:
    subeSensor(token, label.strip() , confidence)
    subeImagen(token, label.strip(), img_id)
    
subeSensor(token, "confidence" , confidence)
print labels

#response = urllib2.urlopen('https://api.instagram.com/v1/tags/pizza/media/XXXXXX')
#data = json.load(response)   
#print data

f.close()

