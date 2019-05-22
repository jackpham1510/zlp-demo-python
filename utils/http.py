import urllib.request, urllib.parse
import json

def PostForm(url, params):
  response = urllib.request.urlopen(url=url, data=urllib.parse.urlencode(params).encode())
  return json.loads(response.read().decode())

def Get(url):
  response = urllib.request.urlopen(url=url)
  return json.loads(response.read().decode())