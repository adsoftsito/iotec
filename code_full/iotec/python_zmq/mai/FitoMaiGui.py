from tkinter import *
import tkMessageBox
import Tkinter as tk
import sys  
sys.path.append('/home/adsoft/modules_fitotron_full/csc')  

from FitoConfig import *
from FitoSendData import *
from FitoGeolocation import *
from FitoWebData import *
from FitoMai import *
from FitoGetImage import *

from PIL import Image, ImageTk
import json

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class FitoMaiGui(Frame):
    
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
    id_planta = 0
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
        self.master.title("MAI - Modulo de adquisicion de Imagenes")


        self.entrytext = StringVar()
        self.entrytext1 = StringVar()
        
        self.myCmdCodebar = Button(self.master, text="Codigo Barras", command=self.showCodeBar).grid(row=0,column=0)

    
        self.myCmdLat = Button(self.master, text="Lateral", command=self.showImgLat)
        self.myCmdLat.grid(row=2,column=0)
        self.myCmdLat.configure(state = DISABLED)

        self.myCmdSup = Button(self.master, text="Superior", command=self.showImgSup)
        self.myCmdSup.grid(row=2,column=1)
        self.myCmdSup.configure(state = DISABLED)    

        self.myCmdSend = Button(self.master, text="Enviar", command=self.sendData)
        self.myCmdSend.grid(row=4,column=0)
        self.myCmdSend.configure(state = DISABLED)
       


 
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

    def showCodeBar(self):
        myImage = FitoGetImage();
        myCodeBar = myImage.getCodeImage();
        self.id_planta = myCodeBar

        myvar=Label(self.master)
        myvar['text'] = self.id_planta
        #myvar.insert(END, self.cloud_api)

        myvar.grid(row=0,column=1)  
        self.myCmdLat.configure(state = NORMAL)      

    def showImgLat(self):
        myImage = FitoGetImage();
        infile = myImage.getImage(0);
        self.url_image0 = infile


        im = Image.open(infile)
        resized = im.resize((200, 200),Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        myvar=Label(self.master,image = tkimage)
        myvar.image = tkimage
        myvar.grid(row=1,column=0)  
        self.myCmdSup.configure(state = NORMAL)      

    def showImgSup(self):
        myImage = FitoGetImage();
        infile = myImage.getImage(1);
        self.url_image1 = infile

        im = Image.open(infile)
        resized = im.resize((200, 200),Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        myvar=Label(self.master,image = tkimage)
        myvar.image = tkimage
        myvar.grid(row=1,column=1)  
        self.myCmdSend.configure(state = NORMAL)

    def sendData(self):
        
        myMai = FitoMai();
        myMsg = myMai.runMaiGui(self.deviceid, self.id_planta, self.url_image0, self.url_image1, self.ip, self.port, self.lat, self.lng);
        self.myCmdLat.configure(state = DISABLED)
        self.myCmdSup.configure(state = DISABLED)
        self.myCmdSend.configure(state = DISABLED)

        tkMessageBox.showinfo("Fitotron - sendData", myMsg)

    def client_exit(self):
        exit()

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.geometry("450x300")

#creation of an instance
app = FitoMaiGui(root)


#mainloop 
root.mainloop()  
