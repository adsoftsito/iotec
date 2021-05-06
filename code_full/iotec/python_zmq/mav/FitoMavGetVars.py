
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class FitoMavGetVars:
   
 def getMavPh(self):
 	myPh = 10
 	# get ph
 	return myPh

 def getMavTemp(self):
 	myTemp = 35
 	# get ph
 	return myTemp

 def getMavCe(self):
 	myCe = 90
 	# get ph
 	return myCe

 def getMavO2(self):
 	myO2 = 15
 	# get ph
 	return myO2

 def getMavCO2(self):
 	myCo2 = 23
 	# get ph
 	return myCo2

 def getMavVars(self):
 	data_vars = Object()       
 	data_vars.ph = self.getMavPh()
 	data_vars.temp = self.getMavTemp()
 	data_vars.ce = self.getMavCe()
 	data_vars.o2 = self.getMavO2()
 	data_vars.co2 = self.getMavCO2()
 	return data_vars
   #data_vars = data_vars.toJSON()
    