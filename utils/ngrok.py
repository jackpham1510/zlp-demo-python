from utils import http
from config import config
import json
import sys

public_url = ""

try:
  res = http.Get(config['ngrok']['tunnels'])
  public_url = res['tunnels'][0]['public_url']
  print('[public_url] ' + public_url)
except:
  print('You must create ngrok public url with `ngrok http 1789` first.')
  sys.exit(1)