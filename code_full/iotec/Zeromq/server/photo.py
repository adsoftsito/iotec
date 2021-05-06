import zmq
import time
import sys
import base64
from subprocess import check_output
import datetime
from pymongo import MongoClient
import gridfs

port = "5556"
if len(sys.argv) > 1:
	port =  sys.argv[1]
	int(port)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)
db = MongoClient().devices
fs = gridfs.GridFS(db)

while True:
	#  Wait for next request from client
	message = socket.recv()
	name = str(datetime.datetime.now()) + ".jpg"
	f = open(name, 'wb')
	ba = bytearray(base64.b64decode(message))
	f.write(ba)
	f.close()
	a = fs.put(str(ba))
	out = check_output(["python", "classify_image.py", "--image_file", name])
	out = out.split('\n')[0] + "[%s]" % a
	rm = check_output(["rm", name])
	socket.send(out)


