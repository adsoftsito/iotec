#from picamera import PiCamera,Color
import httplib2 as http
from urlparse import urlparse

import json


class FitoWebData:

 def getDeviceData(self, cloud_api, deviceid):

  headers = {
    'Content-Type': 'application/json'
  }
  url = cloud_api
  path = "/getdevice?device=" + deviceid
  target = urlparse(url+path)
  method = 'GET'
  body = ''

  #print target
  
  h = http.Http()
  response, content = h.request(
        target.geturl(),
        method,
        body,
        headers)
# assume that content is a json reply
# parse content with the json module
  data = json.loads(content)
  print data
  #djson = json.loads(data)
  return data #['coord']