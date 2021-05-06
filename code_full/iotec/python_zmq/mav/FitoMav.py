from FitoMavGetVars import *

class FitoMav:

 def runMav(self):
 	myDataVars = FitoMavGetVars()
 	values_data = myDataVars.getMavVars()
 	print values_data.ph
 	print values_data.temp
 	print values_data.ce
 	print values_data.o2
 	print values_data.co2
 	return values_data

    
#############################

def main():
	print "running main..."
	myMav = FitoMav()
	#tipoimg = 0
 	myMav.runMav()
 	#runMai(ip, lat, lng)

if __name__ == "__main__":
	print 'running by itself ...'
 	main()
else:
	print 'running imported by another module' 