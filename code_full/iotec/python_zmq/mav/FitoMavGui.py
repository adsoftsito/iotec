from tkinter import *
import tkMessageBox
import Tkinter as tk
import sys  
sys.path.append('/home/adsoft/modules_fitotron_full/csc')  

from FitoConfig import *
from FitoGeolocation import *
from FitoWebData import *
from FitoMavGetVars import * 

from PIL import Image, ImageTk
import json

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class FitoMavGui(Frame):
    
    # config vars
    cloud_api = "";
    appname = "";
    deviceId = "";
    ip = "0.0.0.0";
    port = 0;
    timer = 0;
    lat = 0
    lng = 0

    # device info
    codebar = 0
    url_image0 = ""
    url_image1 = ""
    
    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master
        
        self.init_config();
        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

        

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget    
        self.master.title("MAV - Modulo de adquisicion de Variables")


        self.entrytext = StringVar()
        self.entrytext1 = StringVar()
        
        self.myCmdCodebar = Label(self.master, text="Lectura de Variables").grid(row=0,column=0)
    
        self.myCmdLat = Button(self.master, text="Temp", command=self.getTemp, height = 2, width = 10)
        self.myCmdLat.grid(row=1,column=0)
        self.myCmdLat.configure(state = NORMAL)

        self.myCmdSup = Button(self.master, text="Ph", command=self.getPh, height = 2, width = 10)
        self.myCmdSup.grid(row=2,column=0)
        self.myCmdSup.configure(state = NORMAL)    

        self.myCmdSend = Button(self.master, text="C.E.", command=self.getCe, height = 2, width = 10)
        self.myCmdSend.grid(row=3,column=0)
        self.myCmdSend.configure(state = NORMAL)
       


        self.myCmdSend = Button(self.master, text="O2", command=self.getO2, height = 2, width = 10)
        self.myCmdSend.grid(row=4,column=0)
        self.myCmdSend.configure(state = NORMAL)


        self.myCmdSend = Button(self.master, text="CO2", command=self.getCO2, height = 2, width = 10)
        self.myCmdSend.grid(row=5,column=0)
        self.myCmdSend.configure(state = NORMAL)

        self.myCmdSend = Button(self.master, text="Salir", command=self.client_exit, height = 2, width = 10)
        self.myCmdSend.grid(row=6,column=0)
        self.myCmdSend.configure(state = NORMAL)

 
    def init_config(self):
        myFitoConfig = FitoConfig();
        myData = myFitoConfig.getConfigData();
        #tkMessageBox.showinfo("FitoSmart - Config", myData)
        self.cloud_api = myData['cloud_api'];
        self.appname = myData['appname'];
        self.deviceid = myData['deviceid'];
        self.ip = myData['ip'];
        self.port = myData['port'];
        self.timer = myData['timer'];
        print self.appname
        self.getDeviceData();

    def getDeviceData(self):
        myDeviceData = FitoWebData();
        
        myDevData = myDeviceData.getDeviceData(self.cloud_api, self.deviceid);
        data =  myDevData[0]

        self.description = data['descripcion']
        self.address =  data['calle'] + ", " + data['colonia'] + " " + data['ciudad'] +  " " + data['estado'] + " " + "mexico"
        #self.address =   data['estado'] + "+" + "mexico"
        myGeolocation = FitoGeolocation();
        
        lat, lng = myGeolocation.getGeolocation(self.address);
        self.lat = lat
        self.lng = lng
        print self.lat
        print self.lng

    def getTemp(self):
        myVar = FitoMavGetVars();
        myTemp = myVar.getMavTemp();
        tkMessageBox.showinfo("Temperatura: ", myTemp)
       
    def getPh(self):
        myVar = FitoMavGetVars();
        myPh = myVar.getMavPh();
        tkMessageBox.showinfo("Ph: ", myPh)

    def getCe(self):
        myVar = FitoMavGetVars();
        myCe = myVar.getMavCe();
        tkMessageBox.showinfo("C.E.: ", myCe)

    def getO2(self):
        myVar = FitoMavGetVars();
        myO2 = myVar.getMavO2();
        tkMessageBox.showinfo("O2: ", myO2)

    def getCO2(self):
        myVar = FitoMavGetVars();
        myC02 = myVar.getMavCO2();
        tkMessageBox.showinfo("CO2: ", myCO2)

    def client_exit(self):
        exit()

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.geometry("180x280")

#creation of an instance
app = FitoMavGui(root)


#mainloop 
root.mainloop()  
