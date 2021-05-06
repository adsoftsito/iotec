#from picamera import PiCamera,Color
#import httplib2 as http
#from urlparse import urlparse
import googlemaps
#from googlemaps import GoogleMaps


import json


class FitoGeolocation:

 def getGeolocation(self, address):


  gmaps = googlemaps.Client(key='AIzaSyDWDUcf4fsQETW14FyRhT0-wMHdbyAaP4g')
  #gmaps = GoogleMaps('AIzaSyC8RayL0qVmqFu9NFttSCT5FTEexBdCavQ')

  print address
# Geocoding an address
  geocode_result = gmaps.geocode(address)
  print geocode_result
  #data = json.loads(content)
  lat = geocode_result[0]['geometry']['location']['lat']
  lng = geocode_result[0]['geometry']['location']['lng']
  
  #print data
  #djson = json.loads(data)
  print lat
  print lng 
  return lat, lng #['coord']