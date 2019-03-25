import urllib.request
import json

body = {'network': 'InceptionV1', 'layer': 'mixed4c', 'channel':511}

myurl = "http://localhost:5001/v1/jobs/"

req = urllib.request.Request(myurl)
req.add_header('Content-Type', 'application/json; charset=utf-8')

jsondata = json.dumps(body)
jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

req.add_header('Content-Length', len(jsondataasbytes))

print(jsondataasbytes)
response = urllib.request.urlopen(req, jsondataasbytes)
print(response.read())
