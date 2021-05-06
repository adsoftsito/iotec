class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class FitoActGetVars:
   

 def getActTemp(self):
 	myTemp = 29
 	# get ph
 	return myTemp

 def getActLum(self):
 	myCe = 60
 	# get ph
 	return myCe

 def getMavVars(self):
 	data_vars = Object()       

 	data_vars.temp = self.getActTemp()
 	data_vars.lum = self.getActLum()
 	return data_vars
   #data_vars = data_vars.toJSON()
    