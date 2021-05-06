#from picamera import PiCamera,Color
import httplib2 as http
from urlparse import urlparse
import json


class FitoWeather:

 def getWeather(self, lat, lng):

  headers = {
    'Content-Type': 'application/json'
  }
  url = "http://api.openweathermap.org"
  path = "/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lng) + "&APPID=2af72ef62258728d72777bef612f2a3e&units=metric&lang=es"
  target = urlparse(url+path)
  method = 'POST'
  body = ''

  h = http.Http()

  response, content = h.request(
        target.geturl(),
        method,
        body,
        headers)

  data = json.loads(content)
  print data
  print data['main']
  print data['weather']
  print data['wind']
  #djson = json.loads(data)
  return data['main'], data['weather'], data['wind']