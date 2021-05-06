from FitoSendData import *
from FitoGetImage import *
import sys  
sys.path.append('/home/adsoft/modules_fitotron_full/mav')  

from FitoMav import *

class FitoMai:

 def runMai(self, ip, port, lat, lng):
 	myImage = FitoGetImage()
 	mySend = FitoSendData()
	myVars = FitoMav()

 	code_image = myImage.getCodeImage()

 	url_image0 = myImage.getImage(0)
 	url_image1 = myImage.getImage(1)

 	data_vars = myVars.runMav()
 	
 	myData = mySend.sendData(device_id, id_planta, url_image0, url_image1, data_vars, ip, port, lat, lng);

 def runMaiGui(self, device_id, id_planta, url_image0, url_image1, ip, port, lat, lng):
	myVars = FitoMav()
	mySend = FitoSendData()
 	data_vars = myVars.runMav()
 	myData = mySend.sendData(device_id, id_planta, url_image0, url_image1, data_vars, ip, port, lat, lng);
 	return myData
#############################

def main():
	print "running main..."
	myMai = FitoMai()
	#tipoimg = 0
 	ip = "127.0.0.1"
 	port = 3000
 	lat = 19.6613
 	lng = -96.8875
 	myMai.runMai(ip, port, lat, lng)
 	#runMai(ip, lat, lng)

if __name__ == "__main__":
	print 'running by itself ...'
 	main()
else:
	print 'running imported by another module' 